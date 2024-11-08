from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('filtered_products/', views.filtered_products, name='filtered_products'),
    path('products/', views.products, name='products'),
]
