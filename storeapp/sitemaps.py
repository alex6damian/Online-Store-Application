from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, Discount

class ProductSitemap(Sitemap):
    # Change frequency (ex: always, hourly, daily, weekly, monthly, yearly, never)
    changefreq = "monthly"  
    # Priority (ex: 0.0 - 1.0)
    priority = 0.8        

    def items(self):
        # Returns a QuerySet of all products
        return Product.objects.all()

    def modstock(self, obj):
        # Returns the last time the object was modified
        return obj.stock

class DiscountSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Discount.objects.all()

    def expiration(self, obj):
        return obj.expiration_date
    
class StaticViewsSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['home', 'contact', 'register', 'login']

    def location(self, item):
        return reverse(item)