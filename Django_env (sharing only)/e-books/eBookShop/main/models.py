from django.db import models
from django.utils.html import mark_safe
from django.utils.text import slugify
import random








from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.html import mark_safe
from django.utils.text import slugify
import random








HOMEPAGE_CHOICES = [
    ('product_page', 'Product Page (Princeps Fury)'),
    # Add other homepage options here
]





def generate_isbn():
    while True:
        isbn = random.randint(1000000000000, 9999999999999)
        if not Product.objects.filter(isbn=isbn).exists():
            return isbn


# Genre
class Genre(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = '1. Genres'

    def __str__(self):
        return self.title


# Author
class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = '2. Authors'

    def __str__(self):
        return self.name


# Product
class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='images/')
    pdf_file = models.FileField(upload_to='books/pdfs/', null=True)
    epub_file = models.FileField(upload_to='books/epubs/', null=True)
    isbn = models.BigIntegerField(default=generate_isbn, unique=True)
    detail = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    genres = models.ManyToManyField(Genre)
    status = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)






    motto = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_ratings = models.PositiveIntegerField(default=0)




    class Meta:
        verbose_name_plural = '3. Products'
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="36" height="50" />')
        return "Няма изображение"

    def __str__(self):
        return self.title

class Feedback(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    feedback=models.TextField()
    is_read = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = '4. Feedbacks'














class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=255)
    book_title = models.CharField(max_length=255)
    book_ISBN = models.CharField(max_length=20, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    country = models.CharField(max_length=100, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer_name}"

# Payment
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    special_instructions = models.TextField(blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    # Optional: Payment-specific fields
    card_number = models.CharField(max_length=255, blank=True)
    expiry_date = models.CharField(max_length=10, blank=True)
    cvv = models.CharField(max_length=10, blank=True)
    paypal_username = models.CharField(max_length=255, blank=True)
    bank_name = models.CharField(max_length=255, blank=True)
    account_holder = models.CharField(max_length=255, blank=True)
    account_number = models.CharField(max_length=255, blank=True)
    iban = models.CharField(max_length=255, blank=True)
    swift_bic = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"

# HomepageSetting
class HomepageSetting(models.Model):
    homepage_choice = models.CharField(
        max_length=50,
        choices=HOMEPAGE_CHOICES,
        default='product_page',
        unique=True,
    )

    def __str__(self):
        return f"Active Homepage: {self.get_homepage_choice_display()}"

    def save(self, *args, **kwargs):
        if self._state.adding:
            HomepageSetting.objects.all().delete()
        super().save(*args, **kwargs)

# Rating
class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} stars for {self.product.title} by {self.user.username}"

# Favorite
class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
   
    @property
    def product_slug(self):
        return self.product.slug
    
    @property
    def product_id(self):
        return self.product.id
    
    @property
    def product_image(self):
        return self.product.image
    
    @property
    def product_price(self):
        return self.product.price
    
    @property
    def product_title(self):
        return self.product.title

    @property
    def product_average_rating(self):
        return self.product.average_rating
    
    @property
    def product_total_ratings(self):
        return self.product.total_ratings
    


    class Meta:
        unique_together = ('product', 'user')
        verbose_name_plural = '5. Favourite'

    def __str__(self):
        return f"{self.user.username} favorited {self.product.title}"





















