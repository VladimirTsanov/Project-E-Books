from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.db.models import Count
from django.shortcuts import get_object_or_404
from .models import Product, Category, Brand, Color, Size

def home(request):
    products = Product.objects.all()
    featured_products = Product.objects.filter(featured=True).order_by('-id')
    
    cats = Category.objects.annotate(
        product_count=Count('product', distinct=True)
    )

    brands = Brand.objects.annotate(
        product_count=Count('product', distinct=True)
    )

    colors = Color.objects.annotate(
        product_count=Count('product', distinct=True)
    )

    sizes = Size.objects.annotate(
        product_count=Count('product', distinct=True)
    )
    return render(request, 'index.html',
                  {
                      'products': products,
                      'cats':cats,
                      'brands':brands,
                      'colors':colors,
                      'sizes':sizes,
                      'featured_products':featured_products,
                    })
    
def product_detail(request, slug, id):
    product = get_object_or_404(Product, slug=slug, id=id)
    featured_products = Product.objects.filter(featured=True).order_by('-id')
    
    return render(request, 'product_detail.html', {
        'data':product,
        'featured_products':featured_products,
        })

def  filter_data(request):
    return JsonResponse({'data': 'hello'})