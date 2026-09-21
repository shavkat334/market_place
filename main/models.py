from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_created=True)
    date_edited = models.DateTimeField(auto_created=True)


    def __str__(self):
        return self.category_name



class Products(models.Model):

    product_name = models.CharField(max_length=250)
    product_description = models.TextField()

    product_price_new = models.FloatField(default = 0)
    product_price_old = models.FloatField(default = 0)
    base_price = models.FloatField(default = 0)

    image = models.ImageField(upload_to='product_images')

    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')

    date_created = models.DateTimeField(auto_created=True)
    date_edited = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.product_name
    
    