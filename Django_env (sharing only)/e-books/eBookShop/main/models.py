from django.db import models
from django.utils.html import mark_safe
from django.utils.text import slugify


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
    isbn = models.BigIntegerField(default=1234567890123)
    detail = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

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
