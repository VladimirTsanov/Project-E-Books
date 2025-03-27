from django.db import models
from django.utils.html import mark_safe

# Banner
class Banner(models.Model):
    img=models.CharField(max_length=200)
    alt_text=models.CharField(max_length=300)
    
    class Meta:
        verbose_name_plural='1. Banners'

#Category 
class Category(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="cat_imgs/")
    
    class Meta:
        verbose_name_plural='2. Categories'
    
    def __str__(self):
        return self.title
    
# Brand
class Brand(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="brand_imgs/")
    
    class Meta:
        verbose_name_plural='3. Brands'
    
    def __str__(self):
        return self.title    

# Color
class Color(models.Model):
    title=models.CharField(max_length=100)    
    color_code=models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural='4. Colors'
    
    
    def __str__(self):
        return self.title    

# Size
class Size(models.Model):
    title=models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural='5. Sizes'
        
    def __str__(self):
        return self.title

# Product Model
class Product(models.Model):
    title=models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    slug=models.CharField(max_length=400)
    detail=models.TextField()
    specs=models.TextField()
    price=models.PositiveIntegerField(default=0)

    brand=models.ForeignKey(Brand, on_delete=models.CASCADE)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    color=models.ForeignKey(Color, on_delete=models.CASCADE)
    size=models.ForeignKey(Size, on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    featured=models.BooleanField(default=False)
    
    
    class Meta:
            verbose_name_plural='6. Products'
            
    def image_tag(self):
        return mark_safe('<img src="%s" width="36" height="50" />' % (self.image.url))        
    
    def __str__(self):
        return self.title