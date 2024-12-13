from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .models import Product, Category, CustomUser, Dealer, Promotion
from django.contrib.auth import login, logout
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail, EmailMessage, send_mass_mail, mail_admins
from . import forms
from django.contrib.auth.models import Group, Permission
import random, string, json, datetime, logging
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from .models import PopularProduct
from django.utils import timezone
from .models import Discount

logger=logging.getLogger('django')

# @csrf_exempt - decorator care dezactiveaza verificarea CSRF(cross site request forgery)
def home(request):
    logger.debug('Home view accessed')
    return render(request, 'home.html')


def display_product(request, product_id):
    logger.info(f'Display product view accessed for product_id: {product_id}')
    if request.user.is_authenticated:
        if PopularProduct.objects.filter(user_id=request.user.id).count() >= 5:
            oldest_entry = PopularProduct.objects.filter(user_id=request.user.id).order_by('access_date').first()
            oldest_entry.delete()
        PopularProduct.objects.create(user_id=request.user.id, product_id=product_id, access_date=timezone.now())
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        logger.error(f'Product with id {product_id} does not exist')
        return HttpResponse('Product not found', status=404)
    if product.stock < 5:
        messages.warning(request, 'Only a few items left in stock.')
    return render(request, 'display_product.html', {'product': product})


def products(request):
    logger.debug('Products view accessed')
    form = forms.FilterProductsForm()
    categories = Category.objects.all()
    products = Product.objects.all()
    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products.html', {'form': form, 'page_obj': page_obj, 'categories': categories})


def filter_products(request):
    logger.info('Filter products view accessed')
    if request.method == "POST":
        data = json.loads(request.body)
        form = forms.FilterProductsForm(data)
        if form.is_valid():
            products = Product.objects.all()
            if form.cleaned_data['category']:
                products = products.filter(category=form.cleaned_data['category'])
            if form.cleaned_data['price_range']:
                products = products.filter(price__lte=form.cleaned_data['price_range'])
            
            paginator = Paginator(products, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            products_list = list(page_obj.object_list.values())
            messages.info(request, 'Filters applied successfully.')
            return JsonResponse({'products': products_list})
        else:
            messages.error(request, 'There was an error with your filter.')
    logger.warning('Invalid request in filter_products view')
    return JsonResponse({'error': 'Invalid request'}, status=400)


def contact(request):
    logger.debug('Contact view accessed')
    if request.method == "POST":
        form=forms.ContactForm(request.POST)
        if form.is_valid():
            return redirect('contact_successful')
    else:
        form = forms.ContactForm()
    return render(request, 'contact.html', {'form': form})


def contact_successful(request):
    logger.info('Contact successful view accessed')
    messages.info(request, 'Your message has been sent.')
    return render(request, 'contact_successful.html')


def add_product(request):
    logger.debug('Add product view accessed')
    if request.user.is_authenticated:
            if not request.user.groups.filter(name='Products Admins').exists():
                return HttpResponseForbidden(render(request, '403.html', {'user': request.user,'title': 'Error adding products', 'custom_message': 'You do not have permission to add sneakers.'}))
    else:
        return HttpResponseForbidden(render(request, '403.html', {'custom_message': 'You must be logged in to add sneakers.'}))
    if request.method == "POST":
        form = forms.AddProduct(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            messages.debug(request, 'Product added successfully.')
            return redirect('product_successful')
    else:
        form = forms.AddProduct()
    return render(request, 'add_product.html', {'form': form})
    
def product_successful(request):
    logger.info('Product successful view accessed')
    return render(request, 'add_product_successful.html')


def register_view(request):
    logger.debug('Register view accessed')
    def generate_random_code(length=8):
                letters_and_digits = string.ascii_letters + string.digits
                return ''.join(random.choice(letters_and_digits) for i in range(length))
            
    if request.method == "POST":
        form = forms.RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data.get('username') == 'admin':
                subject = 'Attempt to register with admin username'
                message = f'The email address of the person who tried to register with the username admin is {form.cleaned_data.get('email')}.'
                html_message = f'<h1 style="color:red;">{subject}</h1><p>{message}</p>'
                mail_admins(subject, message, html_message=html_message)
                logger.critical('Attempt to register with admin username')
                return redirect('register')
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.code = generate_random_code()
            confirmation_mail(user)
            user.save()
            messages.debug(request, 'User registered successfully.')
            return redirect('login')
    else:
        form = forms.RegisterForm()
    return render(request, 'register.html', {'form': form})


def confirmation_mail(user):
    logger.debug(f'Sending confirmation mail to {user.email}')
    context = {'first_name': user.first_name,
               'last_name': user.last_name,
               'username': user.username,
               'confirmation_code': user.code,
               }
    html_content = render_to_string('welcome.html', context)
    email = EmailMessage(
        subject='Confirmation email',
        body=html_content,
        from_email='alex6damian@gmail.com',
        to=[user.email]
    )
    email.content_subtype = 'html'
    email.send(fail_silently=False)

def confirm_account(request, code):
    logger.info(f'Confirm account view accessed with code: {code}')
    try:
        user=forms.CustomUser.objects.get(code=code)
        if not user.confirmed_mail:
            user.confirmed_mail = True
            user.save()
            messages.success(request, 'Email confirmed successfully.')
        return redirect('login')
    except forms.CustomUser.DoesNotExist:
        logger.error(f'Invalid confirmation code: {code}')
        return HttpResponse('Invalid confirmation code')



    

def login_view(request):
    logger.debug('Login view accessed')
    if request.method == "POST":
        form = forms.LoginForm(request, data=request.POST)
        user = CustomUser.objects.get(username=form.data['username'])
        if not user.confirmed_mail:
            messages.warning(request, 'Please confirm your email address.')
            return redirect('login')
        if form.is_valid():
            login(request, form.get_user())
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(24*60*60)  # one day
            return redirect('profile')
        else:
            login_attempts = request.session.get('login_attempts', [])
            current_time = timezone.now()
            login_attempts = [attempt for attempt in login_attempts if current_time - datetime.datetime.fromisoformat(attempt) < datetime.timedelta(minutes=2)]
            if len(login_attempts) >= 3:
                subject = 'Suspicious login attempt'
                ip = request.META.get('REMOTE_ADDR')
                message = f'An attempt to login with the username {form.cleaned_data.get("username")} has been made from the IP {ip}.'
                html_message = f'<h1 style="color:red;">{subject}</h1><p>{message}.</p>'
                mail_admins(subject, message, html_message=html_message)
                logger.critical('Suspicious login attempt detected')
                return redirect('login')
            login_attempts.append(current_time.isoformat())
            request.session['login_attempts'] = login_attempts
    else:
        form = forms.LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logger.info('Logout view accessed')
    user = request.user
    user = CustomUser.objects.get(username=user.username)
    if user.has_perm('storeapp.can_check_deal'):
        user.user_permissions.remove(Permission.objects.get(codename='can_check_deal'))
    logout(request)
    messages.error(request, 'You are no longer logged in.')
    return redirect('home')


def change_password(request):
    logger.debug('Change password view accessed')
    if request.method == 'POST':
        form = forms.CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password changed successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Error while changing the password.')
            logger.error('Error while changing the password')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_pwd.html', {'form': form})


def profile(request):
    logger.debug('Profile view accessed')
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
    logger.debug('Edit profile view accessed')
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



def create_promotion(request):
    logger.debug('Create promotion view accessed')
    if request.method == "POST":
        form = forms.PromotionForm(request.POST)
        if form.is_valid():
            try:
                promotion = form.save(commit=False)
                promotion.save()
                messages.success(request, 'Promotion added successfully.')
                
                promotion_categories = form.cleaned_data['combined_choices']
                users = CustomUser.objects.all()
                popular_products = PopularProduct.objects.all()
                data_tuple = []
                for category in promotion_categories:
                    category_id = category.split('_')[1]
                    emails = []
                    for user in users:
                        user_views = popular_products.filter(user_id=user.id, product__category=category_id).count()
                        if user_views >= 3:
                            emails.append(user.email)
                    if emails:
                        subject = f"New Promotion for you!"
                        message = f"Dear Customer, we have a new promotion. Check it out on this link: localhost:8000/storeapp/check_promotion/{promotion.promotion_id}/{category_id}"
                        from_email = 'alex6damian@gmail.com'
                        data_tuple.append((subject, message, from_email, emails))
                print(data_tuple)
                send_mass_mail(data_tuple, fail_silently=False, connection=None)
                return redirect('create_promotion')
            except Exception as e:
                subject = 'Error in create_promotion view'
                message = f'An error occurred: {str(e)}'
                html_message = f'<div style="background-color:red; color:white;"><h1>{subject}</h1><p>{message}</p></div>'
                mail_admins(subject, message, html_message=html_message)
                logger.error(f'Error in create_promotion view: {str(e)}')
    else:
        form = forms.PromotionForm()
    return render(request, 'create_promotion.html', {'form': form})


def check_promotion(request, promotion_id, category_id):
    logger.debug(f'Check promotion view accessed for promotion_id: {promotion_id} and category_id: {category_id}')
    category=Category.objects.get(category_id=category_id)
    promotion = Promotion.objects.get(promotion_id=promotion_id)
    return render(request, 'promotion_template_1.html', {'promotion': promotion, 'category': category})


@login_required
def grant_permission(request):
    if request.method == 'POST':
        if request.user.has_perm('storeapp.can_check_deal'):
            return JsonResponse({'status': 'error', 'message': 'You already claimed the discount code.'}, status=400)
        permission = Permission.objects.get(codename='can_check_deal')
        request.user.user_permissions.add(permission)
        return JsonResponse({'status': 'success', 'message': 'You just got a 50% discount code!', 'redirect_url': 'deal/'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

#@permission_required('storeapp.can_check_deal', login_url=None, raise_exception=False)
def deal(request):
    if request.user.has_perm('storeapp.can_check_deal'):
        random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        Discount.objects.create(code=random_code, rate=50, expiration_date=datetime.date.today() + datetime.timedelta(days=7))
        return render(request, 'deal.html', {'code': random_code})
    else:
        return HttpResponseForbidden(render(request, '403.html', {'title': 'Error checking the deal.', 'custom_message': 'You are not allowed to check this deal.'}))


@csrf_exempt
def cart(request):
    if request.method == 'GET':
        return render(request, 'cart.html')