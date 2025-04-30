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


    if price_filtered:
        context['selected_min_price'] = selected_min_price
        context['selected_max_price'] = selected_max_price

    return render(request, 'index.html', context)


def product_detail(request, slug, id):
    product = get_object_or_404(Product, slug=slug, id=id)
    featured_products = Product.objects.filter(featured=True).order_by('-id')
    
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, product=product).exists()


    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, product=product).first()




    return render(request, 'product_detail.html', {
        'product': product,                             
        'featured_products': featured_products,
        'is_favorited': is_favorited,
        'user_rating': user_rating,
        'show_read_more': len(product.detail) > 400 if product.detail else False,

    })









from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import UserRegisterForm
from django.contrib.auth.decorators import login_required





def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')

            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})








@login_required()
def favorite(request):
    user = request.user
    favorite_products = Favorite.objects.filter(user=user)

    context = {
        'favorite_products': favorite_products,
        
    }

    return render(request, 'favorite.html', context)





















import os


from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math

from .models import Product, Author, Genre, Feedback, Order, Payment, HomepageSetting, Rating, Favorite 

from django.db.models import Q, Avg, Count, Sum, Min, Max
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string 

from django.core.mail import EmailMessage 
from django.conf import settings 
from django.http import FileResponse, Http404, HttpResponseBadRequest, JsonResponse

from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt 

import json 
from django.db import transaction 
from django.urls import reverse 








import json 
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse 

from .models import Product, Order, Payment, HomepageSetting, Rating, Favorite 
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.views.decorators.http import require_POST 
from django.contrib.auth.decorators import login_required 
from django.db.models import Avg, Count, Sum 
from django.db import transaction 
from django.views.decorators.csrf import csrf_exempt 
from django.conf import settings 
from django.core.mail import EmailMessage 
from django.template.loader import render_to_string 

import os 
from django.http import FileResponse, Http404 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, logout, authenticate 
from django.core.exceptions import PermissionDenied 
from django.http import HttpResponseBadRequest 




















@login_required 

def initiate_payment(request, product_id):
    """
    Renders the payment form page for a specific product.
    Accessible to logged-in and anonymous users.
    """

    product = get_object_or_404(Product, id=product_id)
    context = {'product': product} 
  
    return render(request, 'SimplePayment.html', context) 








@csrf_exempt 
@transaction.atomic 
def process_order(request):
    """
    Processes the submitted order and payment information.
    Creates Order and Payment objects and sends a confirmation email with the file.
    Accessible via POST request from logged-in and anonymous users.
    """
    if request.method == 'POST':
       
        product_id = request.POST.get('product_id')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        country = request.POST.get('country')
        chosen_format = request.POST.get('file_format') 
        payment_method = request.POST.get('payment_method')
        special_instructions = request.POST.get('special_instructions')


        if not (product_id and full_name and email and chosen_format):

            print("Missing required form data for order processing.")
            return render(request, 'main/error.html', {'message': 'Missing required information. Please go back and fill all fields.'})



        try:
            product = get_object_or_404(Product, id=product_id)
        except Exception as e:
             print(f"Product with ID {product_id} not found during order processing: {e}")
             return render(request, 'main/error.html', {'message': 'Product not found. Cannot process order.'})



        quantity = 1

        try:
   
            with transaction.atomic():
                order = Order.objects.create(
         
                    user=request.user if request.user.is_authenticated else None,
                    customer_name=full_name,
                    book_title=product.title, 
                    book_ISBN="N/A", 
                    quantity=quantity,
                    total_price=product.price * quantity,
                    country=country,
                    
                )

                payment = Payment.objects.create(
                    order=order, 
                    full_name=full_name,
                    email=email,
                    phone_number=phone_number,
                    country=country,
                    payment_method=payment_method,
                    product_name=product.title, 
                    quantity=quantity, 
                    special_instructions=special_instructions,
                   
                    transaction_id=f"FAKE_TXN_{order.id}", 

                )
            order_processed_successfully = True
            print(f"Order #{order.id} and Payment created successfully for product ID {product_id} for {'authenticated user' if request.user.is_authenticated else 'anonymous user'}.") 
        except Exception as db_error:

            print(f"Error creating Order/Payment objects for product ID {product_id}: {db_error}")

            return render(request, 'main/error.html', {'message': 'Error saving your order information. Please try again.'})



        if order_processed_successfully and email:
            try:
                file_to_attach = None
                file_name = None
                file_mimetype = None


                if chosen_format == 'epub' and product.epub_file and hasattr(product.epub_file, 'path') and os.path.exists(product.epub_file.path):
                    file_to_attach = product.epub_file.path
                    file_name = os.path.basename(product.epub_file.name)
                    file_mimetype = 'application/epub+zip'

                elif chosen_format == 'pdf' and product.pdf_file and hasattr(product.pdf_file, 'path') and os.path.exists(product.pdf_file.path):
                    file_to_attach = product.pdf_file.path
                    file_name = os.path.basename(product.pdf_file.name)
                    file_mimetype = 'application/pdf'


                if file_to_attach:
                    subject = f"Your Order Confirmation and Download for {product.title}"


                    try:
                        body = render_to_string('order_confirmation.txt', {
                            'product': product,
                            'order': order, 
                            'chosen_format': chosen_format.upper(), 
                            'full_name': full_name
                        })


                    except Exception as render_error:
                         print(f"Error rendering email template: {render_error}. Using fallback plain text body.")

                         body = (
                             f"Thank you for your order, {full_name}!\n\n"
                             f"Your Order ID is: {order.id}\n"
                             f"Product: {order.quantity} x {product.title}\n"
                             f"Total: {order.total_price} лв.\n\n"
                             f"Your purchased {chosen_format.upper()} file for {product.title} is attached to this email.\n\n"
                             f"Sincerely,\nThe E-BooX Team"
                         )



                    email_from = settings.DEFAULT_FROM_EMAIL 
                    recipient_list = [email] 


                    email_message = EmailMessage(
                        subject,
                        body, 
                        email_from,
                        recipient_list,

                    )


                    try:
                        with open(file_to_attach, 'rb') as f:
                             email_message.attach(file_name, f.read(), file_mimetype)
                        print(f"Prepared to attach file: {file_name} from {file_to_attach} with mimetype {file_mimetype}") 
                    except FileNotFoundError:
                         print(f"Attachment file not found at {file_to_attach}. Email sent without attachment.")
                    except Exception as attach_error:
                         print(f"Error attaching file {file_to_attach}: {attach_error}. Email sent without attachment.")



                    try:
                        email_message.send(fail_silently=False)
                        print(f"Confirmation email sent successfully to {email} for Order #{order.id}") 
                    except Exception as send_error:

                         print(f"Error sending email for Order #{order.id} to {email}: {send_error}")


                elif chosen_format and not file_to_attach:
                     print(f"Chosen format '{chosen_format}' file path invalid or file not found on disk for product ID {product_id}. Skipping email attachment.")
                elif not chosen_format:
                    print("File format not selected. Skipping email attachment.")


            except Exception as e:

                print(f"An unexpected error occurred during email processing for Order #{order.id}: {e}")

        elif not email:
             print("Email address not provided in form, skipping email sending.")
        elif not order_processed_successfully:
             print("Order/Payment objects not created successfully, skipping email sending.")



        print(f"Redirecting to order success page for Order #{order.id}") 

        return redirect('order_success', order_id=order.id)


    else:

        print("process_order view accessed with non-POST method. Redirecting to homepage/product page.")

        return redirect('home')







@login_required 
def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    product = get_object_or_404(Product, title=order.book_title)

    context = {
        'order': order,
        'product': product,
        'has_epub': product.epub_file and hasattr(product.epub_file, 'url'), 
        'has_pdf': product.pdf_file and hasattr(product.pdf_file, 'url'),
    }
    return render(request, 'order_success.html', context) 















@login_required 
@require_POST
@csrf_exempt 

def rate_product(request, product_id):
    """
    Handles AJAX POST request to submit a product rating.
    Expects 'rating' (1-5) in the POST body JSON.
    Returns updated average rating and total ratings.
    Requires authenticated user.
    """


    try:
        product = get_object_or_404(Product, id=product_id)

        if not request.body:
             return JsonResponse({'status': 'error', 'message': 'Request body is empty.'}, status=400)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
             return JsonResponse({'status': 'error', 'message': 'Invalid JSON body.'}, status=400)

        rating_value = data.get('rating')

        if rating_value is None:
             return JsonResponse({'status': 'error', 'message': 'Rating value missing in JSON body.'}, status=400)

        try:
            rating_value = int(rating_value)
            if not (1 <= rating_value <= 5):
                return JsonResponse({'status': 'error', 'message': 'Rating must be between 1 and 5.'}, status=400)
        except ValueError:
             return JsonResponse({'status': 'error', 'message': 'Invalid rating value. Must be an integer.'}, status=400)


        user = request.user


        existing_rating = Rating.objects.filter(product=product, user=user).first()

        with transaction.atomic():
            if existing_rating:

                old_rating_value = existing_rating.rating
                existing_rating.rating = rating_value
                existing_rating.save()

                current_total_sum = (product.average_rating or 0) * (product.total_ratings or 0)
                new_total_sum = current_total_sum - old_rating_value + rating_value

                product.average_rating = new_total_sum / (product.total_ratings or 1) if (product.total_ratings or 0) > 0 else rating_value


            else:

                Rating.objects.create(product=product, user=user, rating=rating_value)

                current_total_sum = (product.average_rating or 0) * (product.total_ratings or 0)
                new_total_sum = current_total_sum + rating_value
                new_total_ratings_count = (product.total_ratings or 0) + 1

                product.average_rating = new_total_sum / new_total_ratings_count if new_total_ratings_count > 0 else 0.00
                product.total_ratings = new_total_ratings_count

            product.save()


        return JsonResponse({
            'status': 'success',
            'message': 'Rating submitted successfully.',
            'average_rating': round(product.average_rating, 2), 
            'total_ratings': product.total_ratings
        })

    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found.'}, status=404)
    except Exception as e:
        print(f"Error processing rating: {e}")
        return JsonResponse({'status': 'error', 'message': 'An internal error occurred.'}, status=500)



















@login_required 
@require_POST
@csrf_exempt 
def toggle_favorite(request, product_id):
    """
    Handles AJAX POST request to toggle favorite status for a product.
    Requires authenticated user.
    """


    try:
        product = get_object_or_404(Product, id=product_id)
        user = request.user 


        is_favorited = Favorite.objects.filter(product=product, user=user).exists()

        with transaction.atomic():
            if is_favorited:

                Favorite.objects.filter(product=product, user=user).delete()
                message = 'Product removed from favorites.'
                new_is_favorited_status = False
                print(f"User {user.username} unfavorited product {product.title}")
            else:

                Favorite.objects.create(product=product, user=user)
                message = 'Product added to favorites.'
                new_is_favorited_status = True
                print(f"User {user.username} favorited product {product.title}")

        return JsonResponse({
            'status': 'success',
            'message': message,
            'is_favorited': new_is_favorited_status 
        })

    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found.'}, status=404)
    except Exception as e:
        print(f"Error toggling favorite status: {e}")
        return JsonResponse({'status': 'error', 'message': 'An internal error occurred.'}, status=500)




def download_product_file(request, order_id, file_format):
    """
    Serves a purchased digital file (EPUB or PDF) after verifying the order and user.
    """

    if file_format not in ['epub', 'pdf']:
        return HttpResponse("Invalid file format requested.", status=400)

    try:

        order = get_object_or_404(Order, id=order_id)

        product = get_object_or_404(Product, title=order.book_title)


        file_field = getattr(product, f'{file_format}_file', None) 

        if file_field and hasattr(file_field, 'path') and os.path.exists(file_field.path):
            file_path = file_field.path
            file_name = os.path.basename(file_field.name)

            
            if file_format == 'epub':
                mimetype = 'application/epub+zip'
            elif file_format == 'pdf':
                mimetype = 'application/pdf'
            else:
                
                mimetype = 'application/octet-stream' 



            response = FileResponse(open(file_path, 'rb'), content_type=mimetype)
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            print(f"Serving file: {file_path} for order ID {order.id}, format {file_format}") 
            return response

        else:
            print(f"File not found or path invalid for order ID {order.id}, format {file_format}. FilePath: {getattr(file_field, 'path', 'N/A')}")
            return HttpResponse("Requested file not found for this order and format.", status=404)

    except Order.DoesNotExist:
        print(f"Order with ID {order_id} not found for download.")
        raise Http404("Order not found.")
    except Product.DoesNotExist:
        
        print(f"Product not found for order ID {order_id} for download.")
        raise Http404("Product not found for this order.")
    except Exception as e:
        print(f"An unexpected error occurred during file download (Order ID {order_id}, format {file_format}): {e}")
        return HttpResponse("An error occurred while preparing the file for download.", status=500)
















@login_required 
def order_statistics(request):
    if not request.user.is_staff: 
         raise PermissionDenied("You do not have permission to view this page.")


    total_orders = Order.objects.count()
    completed_orders = Order.objects.filter(status='Completed').count()
    total_revenue = Order.objects.filter(status='Completed').aggregate(Sum('total_amount'))['total_amount__sum'] or 0


    orders_data = Order.objects.select_related('user', 'product').order_by('-created_at') 

    context = {
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'total_revenue': total_revenue,
        'orders_data': orders_data,
    }

    return render(request, 'admin/order_statistics.html', context) 

