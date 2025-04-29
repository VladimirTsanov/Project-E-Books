from django.contrib import admin, messages
from .models import Genre, Author, Product, Feedback
from django.utils.text import slugify
from django.utils.html import format_html


admin.site.register(Genre)
admin.site.register(Author)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'colored_is_read')
    readonly_fields = ('name', 'email', 'feedback')
    ordering = ['id']

    def has_add_permission(self, request):
        return False
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if object_id:
            feedback = Feedback.objects.get(id=object_id)
            if not feedback.is_read:
                feedback.is_read = True
                feedback.save(update_fields=['is_read'])
        return super().changeform_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        unread_count = Feedback.objects.filter(is_read=False).count()
        if unread_count > 0:
            self.message_user(request, f"Има {unread_count} непрочетени feedback-a!", messages.WARNING)
        return super().changelist_view(request, extra_context=extra_context)
    
    def render_change_form(self, request, context, *args, **kwargs):
        context['show_save'] = False
        return super().render_change_form(request, context, *args, **kwargs)
    
    def colored_is_read(self, obj):
        if not obj.is_read:
            return format_html(
                '<span style="background-color: #de3731; padding: 5px; border-radius: 3px;">⚠️ Непрочетен</span>'
            )
        return format_html(
                '<span style="background-color: #4cb840; padding: 5px; border-radius: 3px;">Прочетен</span>'
            )
    colored_is_read.short_description = 'Status'

admin.site.register(Feedback, FeedbackAdmin)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display=('id', 'title','slug', 'author', 'display_genres', 'price', 'status', 'featured', 'image_tag')
    filter_horizontal = ('genres',)
    search_fields = ("title", "slug")
    list_editable=('status', 'featured')
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
    
    def display_genres(self, obj):
        return ", ".join([genre.title for genre in obj.genres.all()])
    display_genres.short_description = 'Genres'    
        
admin.site.register(Product, ProductAdmin)
