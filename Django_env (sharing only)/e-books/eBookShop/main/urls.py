from django.urls import path
from . import views
from django.contrib.auth import views as auth_view



urlpatterns = [
    path('',views.home,name='home'),
    path('product-detail/<slug:slug>/<int:id>/', views.product_detail, name='product_detail'),

    path('register/',views.register,name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('favorite/',views.favorite,name='favorite'),



    path('initiate-payment/<int:product_id>/', views.initiate_payment, name='initiate_payment'),

    path('process-order/', views.process_order, name='process_order'),

    path('order-success/<int:order_id>/', views.order_success_view, name='order_success'), 

    path('rate/<int:product_id>/', views.rate_product, name='rate_product'),

    path('favorite/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),

    path('download/<int:order_id>/<str:file_format>/', views.download_product_file, name='download_product_file'),




]