from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q, Min, Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Author, Genre, Feedback
import math

def home(request):
    is_sent = False
    is_error = False
    
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        feedback_text = request.POST.get("feedback")

        if not name or not email or not feedback_text:
            is_error = True
            messages.error(request, "Всички полета са задължителни.")
        else:
            try:
                Feedback.objects.create(
                    name=name,
                    email=email,
                    feedback=feedback_text
                )
                is_sent = True
                is_error = False
            except Exception as e:
                is_error = True
                messages.error(request, f"Неуспех: {str(e)}")
    
        return redirect('home')
    
        
    # Основни продукти
    products = Product.objects.all()

    # Филтри за автори и жанрове
    selected_authors = request.GET.getlist('author')
    selected_genres = request.GET.getlist('genre')
    show_only_featured = request.GET.get('featured') == 'true'
    featured_counter = Product.objects.filter(featured=True).count()

    # Ценови граници от всички продукти
    raw_min = Product.objects.aggregate(Min('price'))['price__min'] or 0
    raw_max = Product.objects.aggregate(Max('price'))['price__max'] or 0

    all_min_price = math.floor(raw_min)
    all_max_price = math.ceil(raw_max)

    # Взимане на избраните цени от URL
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Стойности за темплейта (по подразбиране)
    selected_min_price = all_min_price
    selected_max_price = all_max_price

    price_filtered = False
    try:
        if min_price is not None:
            min_price = int(min_price)
        if max_price is not None:
            max_price = int(max_price)

        if min_price is not None and max_price is not None:
            # Ако потребителят е задал диапазон, филтрираме
            if min_price > all_min_price or max_price < all_max_price:
                price_filtered = True
                selected_min_price = min_price
                selected_max_price = max_price
                products = products.filter(price__gte=min_price, price__lte=max_price)

    except ValueError:
        min_price = None
        max_price = None

    # Търсачка
    query = request.GET.get('q', '')
    if query and query.strip() != '':
        products = products.filter(
            Q(title__icontains=query) |
            Q(detail__icontains=query) |
            Q(author__name__icontains=query)
        )
    else:
        if 'q' in request.GET:
            return redirect('home')

    # Филтри по автори и жанрове
    if selected_authors:
        products = products.filter(author__id__in=selected_authors)
    if selected_genres:
        products = products.filter(genres__id__in=selected_genres)
    if show_only_featured:
        products = products.filter(featured=True)
        
        # Ето тук динамично вземаме възможните жанрове и автори
    available_genres = Genre.objects.filter(product__in=products).distinct()
    available_authors = Author.objects.filter(product__in=products).distinct()
    available_genres = available_genres.annotate(product_count=Count('product'))
    available_authors = available_authors.annotate(product_count=Count('product'))


    authors = Author.objects.annotate(product_count=Count('product', distinct=True)).order_by('name')
    genres = Genre.objects.annotate(product_count=Count('product', distinct=True)).order_by('title')

    no_results = products.count() == 0

    # Сортиране
    sort = request.GET.get('sortBy', 'newest')
    if sort == 'lowestPrice':
        products = products.order_by('price')
    elif sort == 'highestPrice':
        products = products.order_by('-price')
    elif sort == 'bestSelling':
        products = products.annotate(sales_count=Count('order_items')).order_by('-sales_count')
    else:
        products = products.order_by('-id')
        
        

    # Пагинация
    try:
        per_page = int(request.GET.get('itemsPerPage', 12))
    except (ValueError, TypeError):
        per_page = 12

    paginator = Paginator(products, per_page)

    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Проверка дали има други активни филтри
    other_filtered = any(param in request.GET for param in ['genre', 'author', 'q', 'featured'])
    is_filtered = other_filtered or price_filtered

    context = {
        'products': page_obj.object_list,
        'authors': authors,
        'genres': genres,
        'selected_authors': list(map(int, selected_authors)),
        'selected_genres': list(map(int, selected_genres)),
        'available_genres': available_genres,
        'available_authors': available_authors,
        'all_min_price': all_min_price,
        'all_max_price': all_max_price,
        'show_only_featured': show_only_featured,
        'price_filtered': price_filtered,
        'is_filtered': is_filtered,
        'no_results': no_results,
        'page_obj': page_obj,
        'per_page': per_page,
        'items_per_page': per_page,
        'sort': sort,
        'is_sent': is_sent,
        'is_error':is_error,
        'featured_counter': featured_counter,
    }

    # Само ако цените са филтрирани, пращаме в темплейта
    if price_filtered:
        context['selected_min_price'] = selected_min_price
        context['selected_max_price'] = selected_max_price

    return render(request, 'index.html', context)


def product_detail(request, slug, id):
    product = get_object_or_404(Product, slug=slug, id=id)
    featured_products = Product.objects.filter(featured=True).order_by('-id')

    return render(request, 'product_detail.html', {
        'data': product,
        'featured_products': featured_products,
    })
