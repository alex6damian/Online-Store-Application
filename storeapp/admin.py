from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Customizing the admin interface
class ProductAdmin(admin.ModelAdmin):
    fieldsets = ( # group fields together
        ('General Information', {
            'fields': ('name', 'price', 'stock', 'image_url')
        }),
        ('More Information', {
            'fields': ('dealer', 'category')
        }
        )
    )
    search_fields = ('name', 'price') # search by name and price
    list_filter = ('category', 'dealer') # filter by category and dealer

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',) # search by name

class DealerAdmin(admin.ModelAdmin):
    fieldsets = ( # group fields together
        ('General Information', {
            'fields': ('name',)
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address') 
        })
    )
    search_fields = ('name', 'phone') # search by name and phone

class DiscountAdmin(admin.ModelAdmin):
    search_fields = ('code', 'rate') # search by code and rate
    ordering = ('expiration_date',) # order by expiration_date
    
class OrderAdmin(admin.ModelAdmin):
    search_fields = ('order_id',) # search by order_id
    ordering = ('order_date',) # order by order_date


        

# Register models
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Dealer, DealerAdmin)
admin.site.register(models.Discount, DiscountAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.CustomUser, UserAdmin)

# Customize the admin site
admin.site.site_header = 'Store App Administration'
admin.site.site_title = 'Store App Admin'
admin.site.index_title = 'Welcome to Store App Admin Page'