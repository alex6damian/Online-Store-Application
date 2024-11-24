from django.http import HttpResponse
import datetime
from django.core.paginator import Paginator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import login, logout
from . import forms

# @csrf_exempt - decorator care dezactiveaza verificarea CSRF(cross site request forgery)
def home(request):
    return render(request, 'home.html')

def filtered_products(request):
    filtered_products = Product.objects.filter(category__name__exact='shoes')

    filtered_products = filtered_products.filter(price__gt=100, price__lt=800)
    
    if request.method == "POST":
        prod = forms.ProductForm(request.POST)
        if prod.is_valid():    
            return render(request, 'products.html', {'products':prod})
    else:
        prod = forms.ProductForm()
    return render(request, 'products.html', {'products':prod})

def products(request):
    products = Product.objects.all()
    paginator = Paginator(products, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products.html', {'products':page_obj})

def contact(request):
    if request.method == "POST":
        form=forms.ContactForm(request.POST)
        if form.is_valid():
            return redirect('contact_successful')
    else:
        form = forms.ContactForm()
    return render(request, 'contact.html', {'form': form})

def contact_successful(request):
    return render(request, 'contact_successful.html')

def add_product(request):
    if request.method == "POST":
        form = forms.AddProduct(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('product_successful')
    else:
        form = forms.AddProduct()
    return render(request, 'add_product.html', {'form': form})
    
def product_successful(request):
    return render(request, 'add_product_successful.html')

def register_view(request):
    if request.method == "POST":
        form = forms.RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = forms.RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = forms.LoginForm(data=request.POST, request=request)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(24*60*60)  # one day
            return redirect('profile')
    else:
        form = forms.LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def change_password(request):
    if request.method == 'POST':
        form = forms.CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password changed successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Error while changing the password.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_pwd.html', {'form': form})


def profile(request):
    if not request.user.is_authenticated:
            return redirect('login')
    user_data = request.session.get('user_data', {})
    if not user_data:
        user_data = {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        request.session['user_data'] = user_data
            
    return render(request, 'profile.html', {'user_data': user_data})

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = forms.EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = forms.EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})