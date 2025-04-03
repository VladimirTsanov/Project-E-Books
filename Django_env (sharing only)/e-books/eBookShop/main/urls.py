from django.urls import path
from . import views



urlpatterns = [
    path('',views.home,name='home'),
    path('product-detail/<str:slug>/<int:id>',views.product_detail, name='product_detail'),
    path('filter-data',views.filter_data, name='filter_data'),
]

