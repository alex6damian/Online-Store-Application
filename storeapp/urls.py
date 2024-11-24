from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('filtered_products/', views.filtered_products, name='filtered_products'),
    path('products/', views.products, name='products'),
    path('contact/', views.contact, name='contact'),
    path('contact_successful/', views.contact_successful, name='contact_successful'),
    path('add_product/', views.add_product, name='add_product'),
    path('product_successful/', views.product_successful, name='product_successful'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)