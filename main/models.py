from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_created=True)
    date_edited = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = "Categories"


class Products(models.Model):
    product_name = models.CharField(max_length=250)
    product_description = models.TextField()

    product_price_new = models.FloatField(default=0)
    product_price_old = models.FloatField(default=0)
    base_price = models.FloatField(default=0)

    image = models.ImageField(upload_to='product_images')

    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')

    date_created = models.DateTimeField(auto_created=True)
    date_edited = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name_plural = "Products"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"
    
    def get_total_price(self):
        return self.product.product_price_new * self.quantity