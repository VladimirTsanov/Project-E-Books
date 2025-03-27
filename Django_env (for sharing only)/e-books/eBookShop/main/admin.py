from django.contrib import admin
from .models import Banner, Category,Brand,Color, Size, Product

admin.site.register(Banner)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Size)

class ProductAdmin(admin.ModelAdmin):
    list_display=('id', 'title', 'brand', 'color', 'size', 'price', 'status', 'featured', 'image_tag')
    list_editable=('status', 'featured',)
admin.site.register(Product, ProductAdmin)
