from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import ProductSitemap, StaticViewsSitemap, DiscountSitemap

sitemaps = {
    'products': ProductSitemap,
    'disscounts': DiscountSitemap,
    'static': StaticViewsSitemap,
}

urlpatterns = [
    path('', views.home, name='home'),
    path('filter_products/', views.filter_products, name='filter_products'),
    path('products/', views.products, name='products'),
    path('product/<int:product_id>/', views.display_product, name='display_product'),
    path('contact/', views.contact, name='contact'),
    path('contact_successful/', views.contact_successful, name='contact_successful'),
    path('add_product/', views.add_product, name='add_product'),
    path('product_successful/', views.product_successful, name='product_successful'),
    path('register/', views.register_view, name='register'),
    path('confirm/<str:code>/', views.confirm_account, name='confirm_account'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('promotions/', views.create_promotion, name='create_promotion'),
    path('check_promotion/<int:promotion_id>/<int:category_id>/', views.check_promotion, name='check_promotion'),
    path('grant_permission/', views.grant_permission, name='grant_permission'),
    path('deal/', views.deal, name='deal'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('cart/', views.cart, name='cart'),
    path('data_processing/', views.data_processing, name='data_processing'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)