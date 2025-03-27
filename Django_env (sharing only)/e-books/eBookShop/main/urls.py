from django.urls import path
from . import views



urlpatterns = [
    path('',views.home,name='home'),
    path('product-detail/<str:slug>/<int:id>',views.product_detail, name='product_detail'),
]

