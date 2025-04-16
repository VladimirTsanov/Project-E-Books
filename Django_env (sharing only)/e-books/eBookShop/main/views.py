from django.shortcuts import render
from django.db.models import Count, Q, Min, Max
from django.shortcuts import get_object_or_404
from .models import Product, Author, Genre

def home(request):
    is_filtered = any(param in request.GET for param in ['genre', 'author', 'min_price', 'max_price'])
    
    
    # Взимаме избраните стойности от GET параметрите
    selected_authors = request.GET.getlist('author')
    selected_genres = request.GET.getlist('genre')
    show_only_featured = request.GET.get('featured') == 'true'
    featured_counter = Product.objects.filter(featured=True).count()
    min_price = request.GET.get('min_price') or request.GET.get('min_price_text')
    max_price = request.GET.get('max_price') or request.GET.get('max_price_text')

    # Начално queryset
    products = Product.objects.all()
    
    query = request.GET.get('q', '')
    
    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(detail__icontains=query) |
            Q(author__name__icontains=query)
            
        )
        is_filtered = True
            
    # Филтриране по ценовия диапазон
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)
        
    try:
        min_price = float(min_price)
    except (TypeError, ValueError):
        min_price = None

    try:
        max_price = float(max_price)
    except (TypeError, ValueError):
        max_price = None

    # Филтриране по останалите категории
    if selected_authors:
        products = products.filter(author__id__in=selected_authors)
    if selected_genres:
        products = products.filter(genre__id__in=selected_genres)
    if show_only_featured:
        products = products.filter(featured=True)

    # Получаваме минималната и максималната цена
    all_min_price = products.aggregate(Min('price'))['price__min']
    all_max_price = products.aggregate(Max('price'))['price__max']

    # Филтри с брой продукти
    authors = Author.objects.annotate(product_count=Count('product', distinct=True)).order_by('name')
    genres = Genre.objects.annotate(product_count=Count('product', distinct=True)).order_by('title')

    no_results = products.count() == 0

    return render(request, 'index.html', {
        'products': products,
        'authors': authors,
        'genres': genres,
        'selected_authors': list(map(int, selected_authors)),
        'selected_genres': list(map(int, selected_genres)),
        'all_min_price': all_min_price,
        'all_max_price': all_max_price,
        'show_only_featured' : show_only_featured,
        'is_filtered': is_filtered,
        'no_results': no_results,
        'featured_counter' : featured_counter,
        'selected_min_price': min_price if min_price is not None else all_min_price,
        'selected_max_price': max_price if max_price is not None else all_max_price,

})
    
def product_detail(request, slug, id):
    product = get_object_or_404(Product, slug=slug, id=id)
    # Извлича продукти за допълнително показване
    featured_products = Product.objects.filter(featured=True).order_by('-id')
    
    return render(request, 'product_detail.html', {
        'data': product,
        'featured_products': featured_products,
    })
