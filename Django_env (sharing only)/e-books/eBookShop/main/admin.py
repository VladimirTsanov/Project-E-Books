from django.contrib import admin
from .models import Genre, Author, Product
from django.utils.text import slugify


admin.site.register(Genre)
admin.site.register(Author)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display=('id', 'title','slug', 'author', 'genre', 'price', 'status', 'featured', 'image_tag')
    search_fields = ("title", "slug")
    list_editable=('status', 'featured',)
    ordering = ['id']
    
    def save_model(self, request, obj, form, change):
        if not obj.slug:
            base_slug = slugify(obj.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(id=obj.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            obj.slug = slug
        super().save_model(request, obj, form, change)
        
admin.site.register(Product, ProductAdmin)
