from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from . import models
from .models import CustomUser
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

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

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('phone', 'address', 'birth_date')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('phone', 'address', 'birth_date')
        }),
    )
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_active')  # display these fields in the list view
    list_editable = ('first_name', 'last_name', 'email')  # make these fields editable in the list view
    actions = ['block_users', 'unblock_users']  # add custom actions

    def block_users(self, request, queryset):
        queryset.update(is_active=False)
    block_users.short_description = 'Block selected users'

    def unblock_users(self, request, queryset):
        queryset.update(is_active=True)
    unblock_users.short_description = 'Unblock selected users'


group_name = 'Products Admins' # group name
if not Group.objects.filter(name=group_name).exists(): # check if the group exists
    products_admins = Group.objects.create(name='Products Admins') # create a group
    permissions = Permission.objects.all() # get all permissions
    products_admins.permissions.set(permissions) # set permissions to the group
    group_member = CustomUser.objects.get(username='administrator') # get a user
    group_member.groups.add(products_admins) # add the user to the group 

group_name = 'Moderators' # group name
if not Group.objects.filter(name=group_name).exists(): # check if the group exists
    moderators = Group.objects.create(name='Moderators') # create a group
    group_member = CustomUser.objects.get(username='moderator') # get a user
    group_member.groups.add(moderators) # add the user to the group
    group_member.is_staff = True # make the user staff

# Create a new permission
permission_name = 'Can check deal'
permission_codename = 'can_check_deal'
content_type = ContentType.objects.get_for_model(models.Product)
if not Permission.objects.filter(codename=permission_codename).exists():
    Permission.objects.create(
        codename=permission_codename,
        name=permission_name,
        content_type=content_type,
    )


# Register models
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Dealer, DealerAdmin)
admin.site.register(models.Discount, DiscountAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.CustomUser, CustomUserAdmin)


# Customize the admin site
admin.site.site_header = 'Store App Administration'
admin.site.site_title = 'Store App Admin'
admin.site.index_title = 'Welcome to Store App Admin Page'