from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20)
    rate = models.FloatField()
    expiration_date = models.DateField()

    def __str__(self):
        return self.code



class Dealer(models.Model):
    dealer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    address = models.CharField(max_length=255, default=None, null=True)
    
    def __str__(self):
        return self.name



class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.name



class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    image_url = models.CharField(max_length=2083)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    order = models.ManyToManyField('Order', related_name='order', default=None)
    
    def __str__(self):
        return self.name



class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    product = models.ManyToManyField(Product, related_name='product', default=None)
    order_date = models.DateField()
    
    def __str__(self):
        return str(self.order_id) 
    

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    birth_date = models.DateField(null=False, blank=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Adaugă related_name pentru a evita conflictul
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Adaugă related_name pentru a evita conflictul
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )

    def __str__(self):
        return self.username