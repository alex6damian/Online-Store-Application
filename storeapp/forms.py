from django import forms
from django.db import models
from .models import Dealer, Category, Product, CustomUser, Promotion
from datetime import date
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
import json, time, os, re
from django.contrib.auth import authenticate
from datetime import datetime
from django.contrib.auth.forms import PasswordChangeForm

class ProductForm(forms.Form):
    name = forms.CharField(max_length=255,required=True ,label = 'Product Name')
    price = forms.FloatField(label='Price', )
    stock = forms.IntegerField(label='Stock', required=True)
    image_url = forms.CharField(max_length=2083, label='Image URL', required=True)
    dealer = forms.ModelChoiceField(queryset=Dealer.objects.all(), required=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    
    
    def clean(self):
        cleaned_data = super().clean()
        name= cleaned_data.get('name')
        price = cleaned_data.get('price')
        stock = cleaned_data.get('stock')
        image_url = cleaned_data.get('image_url')
        dealer = cleaned_data.get('dealer')
        category = cleaned_data.get('category')
        if name is None:
            raise forms.ValidationError('Name must be a string')
        if price < 0:
            raise forms.ValidationError('Price must be a positive number')
        if stock < 0:
            raise forms.ValidationError('Stock must be a positive number')
        if not name or not price or not stock or not image_url or not dealer or not category:
            raise forms.ValidationError('All fields are required')
        if dealer is None:
            raise forms.ValidationError('Dealer must be selected')
        if category is None:
            raise forms.ValidationError('Category must be selected')
        return cleaned_data

class FilterProductsForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        required=False, 
        empty_label="Select a category"
    )
    only_in_stock = forms.BooleanField(required=False, label='Only in stock')
    price_range = forms.FloatField(
        initial = 0,
        min_value = 0,
        max_value = 1000,
        widget=forms.NumberInput(attrs={'type': 'range', 'min': '0', 'max': '1000', 'step': '10'}),
        required=False,
        label='Price Range'
    )
    def clean(self):
        cleaned_data = super().clean()
        price_range = cleaned_data.get('price_range')
        if price_range is not None and (price_range < 0 or price_range > 10000):
            raise forms.ValidationError('Price range must be between 0 and 10000')
        return cleaned_data

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=10, required=True, label = 'First Name')
    second_name = forms.CharField(max_length=15, required=True, label = 'Second Name')
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label='Birth Date'
    )
    email = forms.EmailField(required=True, label = 'Email')
    confirmed_email = forms.EmailField(required=True, label = 'Confirm Email')
    message_type_choises = [
        ('complaint', 'Complaint'),
        ('question', 'Question'),
        ('review', 'Review'),
        ('request', 'Request'),
        ('appoinment', 'Appoinment'),
    ]
    message_type = forms.ChoiceField(choices=message_type_choises, required=True, label = 'Message Type')
    subject = forms.CharField(max_length=15, required=True, label = 'Subject')
    waiting_time = forms.IntegerField(required=True, label = 'Waiting Time')
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}), required=True, label='Message')

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        second_name = cleaned_data.get('second_name')
        birth_date = cleaned_data.get('birth_date')
        email = cleaned_data.get('email')
        confirmed_email = cleaned_data.get('confirmed_email')
        subject = cleaned_data.get('subject')
        waiting_time = cleaned_data.get('waiting_time')
        message = cleaned_data.get('message')
        
        if email != confirmed_email:
            raise forms.ValidationError('Emails do not match')
        today=date.today()
        if today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day)) < 18:
            raise forms.ValidationError('You must be at least 18 years old')
        
        if not re.match(r"^(\b\w+\b[\s,.]*){5,100}$", message):
            raise forms.ValidationError('Message must be between 5 and 100 words')
        if re.search(r"\bhttps?://", message):
            raise forms.ValidationError('Message cannot contain URLs')
        if waiting_time < 0:
            raise forms.ValidationError('Waiting time must be a positive number')
    
        def validate_text(text):
            if not re.match(r"^[A-Z][a-z\s]+$", text):
                raise forms.ValidationError('Names and subject must start with a capital letter and contain only letters and spaces')
        
        validate_text(first_name)
        if second_name:
            validate_text(second_name)
        validate_text(subject)
        
        if birth_date:
            today = date.today()
            age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            age_months = today.month - birth_date.month - (today.day < birth_date.day)
            if age_months < 0:
                age_months += 12
            cleaned_data['age'] = f'{age_years} years and {age_months} months'
        if message:
            message = ' '.join(message.split())
            cleaned_data['message'] = message
        
        data_to_save = {
            'first_name': cleaned_data.get('first_name'),
            'second_name': cleaned_data.get('second_name'),
            'age': cleaned_data.get('age'),
            'email': cleaned_data.get('email'),
            'message_type': cleaned_data.get('message_type'),
            'subject': cleaned_data.get('subject'),
            'waiting_time': cleaned_data.get('waiting_time'),
            'message': cleaned_data.get('message'),
        }

        timestamp = int(time.time())
        filename = f"mesaj_{timestamp}.json"
        messages_dir = os.path.join(os.path.dirname(__file__), 'messages')
        if not os.path.exists(messages_dir):
            os.makedirs(messages_dir)
            
        filename = os.path.join(messages_dir, filename)
        with open(filename, 'w') as json_file:
            json.dump(data_to_save, json_file, indent=4)
        
        return cleaned_data

class AddProduct(forms.ModelForm):
    
    field1 = forms.IntegerField(required=True, label = 'TVA')
    field2 = forms.IntegerField(required=True, label = 'Stock for promotion')
    
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'image_url', 'category', 'dealer']
        labels = {
            'name': 'Product Name',
            'price': 'Price ($)',
            'stock': 'Stock',
            'image_url': 'Image URL',
            'category' : 'Category',
            'dealer' : 'Dealer',
            }
        help_texts = {
            'name': 'Enter the product name. Only letters and spaces are allowed.',
            'price': 'Enter the price of the product. Must be a positive number.',
            'stock': 'Enter the stock quantity. Must be a positive number.',
            'image_url': 'Enter the image URL of the product.',
            'category' : 'Select the category of the product.',
            'dealer' : 'Select the dealer of the product.',
            
        }
        error_messages = {
            'name': {
                'required': 'Your name is required and must be a string',
            },
            'price': {
                'required': 'Price must be a positive number',
            },
            'stock': {
                'required': 'Stock must be a positive number',
            },
            'image_url': {
                'required': 'Image URL is required',
            },
            'category': {
                'required': 'Category must be selected',
            },
            'dealer': {
                'required': 'Dealer must be selected',
            }
        }
        
        
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        stock = cleaned_data.get('stock')
        dealer = cleaned_data.get('dealer')
        category = cleaned_data.get('category')
        tva = cleaned_data.get('field1')
        stock_promotion = cleaned_data.get('field2')
        # validation that uses 2 fields
        if price is not None and stock is not None:
            if price <=0 and stock <=0:
                raise forms.ValidationError('Price and stock must be positive numbers')
        
        # 3 validation rules
        if not re.match(r'^[A-Za-z0-9\s]+$', name):
            raise forms.ValidationError('Name must contain only letters and spaces')
        if len(name) < 3:
            raise forms.ValidationError('Name must be at least 3 characters long')
        if price is None or price < 0:
            raise forms.ValidationError('Price must be a positive number')
        if stock is None or stock < 0:
            raise forms.ValidationError('Stock must be a positive number')
        if category is None or dealer is None:
            raise forms.ValidationError('All fields are required')
        if stock_promotion > stock:
            raise forms.ValidationError('Stock for promotion must be less than the stock')
        
        # updating price
        cleaned_data['price'] = price + price * tva / 100
        
        # updating stock
        cleaned_data['stock'] = stock - stock_promotion
        
        return cleaned_data

class RegisterForm(UserCreationForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label='Birth Date'
        ) 
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'birth_date', 'profile_picture', 'bio']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': 'Phone Number',
            'address': 'Address',
            'birth_date': 'Birth Date',
            'profile_picture': 'Profile Picture',
            'bio': 'Bio',
        }
        widgets = {
            'bio' : forms.Textarea(attrs={'rows': 2, 'cols': 40}),
        }
        help_texts = {
            'username': 'Enter your username. Only letters, digits and @/./+/-/_ are allowed.',
            'email': 'Enter your email address.',
            'phone_number': 'Enter your phone number.',
        }
        error_messages = {
            'username': {
                'required': 'Your username is required and must be a string',
                'invalid': 'Username must contain only letters, digits and @/./+/-/_',
            },
            'email': {
                'required': 'Email is required',
                'invalid': 'Email must be a valid email address',
            },
            'first_name': {
                'invalid': 'First name must contain only letters and spaces',
            },
            'last_name': {
                'invalid': 'Second name must contain only letters and spaces',
            },
            'phone_number': {
                'required': 'Phone number is required',
                'invalid': 'Phone number must start with 0 and contain 10 digits',
            },
            'birth_date': {
                'required': 'Birth date is required',
                'invalid': 'Birth date must be in the past',
            },
            'address': 
            {
                'invalid': 'Address must contain only letters, digits and spaces',
            },
        }  
        
    def clean(self):
        cleaned_data=super().clean()
        username = cleaned_data.get('username')
        phone_number = cleaned_data.get('phone_number')
        address = cleaned_data.get('address')
        birth_date = cleaned_data.get('birth_date')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        
        
        if username and not re.match(r'^[A-Za-z0-9\S]+$', username):
            self.add_error('username', self.Meta.error_messages['username']['invalid'])
        if phone_number and not re.match(r'^[0]{1}[0-9]{9}+$', phone_number):
            self.add_error('phone_number', self.Meta.error_messages['phone_number']['invalid'])
        if address and not re.match(r'^[A-Za-z0-9\s,-]+$', address):
            self.add_error('address', self.Meta.error_messages['address']['invalid'])
        if birth_date and birth_date > date.today():
            self.add_error('birth_date', self.Meta.error_messages['birth_date']['invalid'])
        if first_name and not re.match(r'^[A-Za-z\s]+$', first_name):
            self.add_error('first_name', self.Meta.error_messages['first_name']['invalid'])
        if last_name and not re.match(r'^[A-Za-z\s]+$', last_name):
            self.add_error('last_name', self.Meta.error_messages['last_name']['invalid'])
        
        return cleaned_data

class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        label='Remember me')
    def clean(self):
        cleaned_data = super().clean()
        remember_me = cleaned_data.get('remember_me')
        return cleaned_data

class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if len(password1) < 10:
            raise forms.ValidationError("Password needs to have at least 10 characters.")
        return password1
    
class EditProfileForm(UserChangeForm):
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'address', 'profile_picture', 'bio']
        widgets = {
            'first_name': forms.TextInput(attrs={'required': False}),
            'last_name': forms.TextInput(attrs={'required': False}),
            'address': forms.TextInput(attrs={'required': False}),
            'bio': forms.Textarea(attrs={'required': False, 'rows': 2, 'cols': 40}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'address': 'Address',
            'profile_picture': 'Profile Picture',
            'bio': 'Bio',
        }
        error_messages = {
            'first_name': {
                'invalid': 'First name must contain only letters and spaces',
            },
            'last_name': {
                'invalid': 'Last name must contain only letters',
            },
            'address': {
                'invalid': 'Address must contain only letters, digits and spaces',
            },
            'bio': {
                'invalid': 'Bio must contain only letters, digits and spaces',
            },
        }
    
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        if 'password' in self.fields:
            self.fields.pop('password')
    
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        address = cleaned_data.get('address')
        bio = cleaned_data.get('bio')
        
        first_name = cleaned_data.get('first_name')
        first_name = first_name.split(" ")
        first_name = " ".join(first_name)
        if first_name and not re.match(r'^[A-Za-z\s]+$', first_name):
            self.add_error('first_name', self.Meta.error_messages['first_name']['invalid'])
        if last_name and not re.match(r'^[A-Za-z]+$', last_name):
            self.add_error('last_name', self.Meta.error_messages['last_name']['invalid'])
        if address and not re.match(r'^[A-Za-z0-9\s,-]+$', address):
            self.add_error('address', self.Meta.error_messages['address']['invalid'])
        if bio and not re.match(r'^[A-Za-z0-9,.!\s]+$', bio):
            self.add_error('bio', self.Meta.error_messages['bio']['invalid'])
        
        return cleaned_data
    
class PromotionForm(forms.ModelForm):
    combined_choices = forms.MultipleChoiceField(
        choices=[],
        required=True,
        widget=forms.CheckboxSelectMultiple,
        label='Options',
    )
    class Meta:
        model = Promotion
        fields = ['name', 'message', 'start_date', 'end_date', 'discount', 'description']
        labels = {
            'name': 'Promotion Name',
            'message': 'Message',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'discount': 'Discount',
            'description': 'Description',
        }
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'name': 'Enter the promotion name. Only letters and spaces are allowed.',
            'message': 'Enter the message for the promotion.',
            'discount': 'Enter the discount rate. Must be a positive number.',
            'description': 'Enter the description of the promotion.',
        }
        error_messages = {
            'name': {
                'required': 'Promotion name is required',
            },
            'message': {
                'required': 'Message is required',
            },
            'discount': {
                'required': 'Discount is required',
            },
            'description': {
                'required': 'Description is required',
            },
        }

    def __init__(self, *args, **kwargs):
        super(PromotionForm, self).__init__(*args, **kwargs)
        categories = Category.objects.all()
        dealers = Dealer.objects.all()
        combined_choices = [(f'category_{category.category_id}', f'Category: {category.name}') for category in categories]
        combined_choices += [(f'dealer_{dealer.dealer_id}', f'Brand: {dealer.name}') for dealer in dealers]
        self.fields['combined_choices'].choices = combined_choices
        
        # Set default selected choices
        default_selected = [choice[0] for choice in combined_choices]
        self.fields['combined_choices'].initial = default_selected

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        message = cleaned_data.get('message')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        discount = cleaned_data.get('discount')
        description = cleaned_data.get('description')
        combined_choices = cleaned_data.get('combined_choices')

        if not re.match(r'^[A-Za-z\s]+$', name):
            raise forms.ValidationError('Name must contain only letters and spaces')
        if len(name) < 3:
            raise forms.ValidationError('Name must be at least 3 characters long')
        if not re.match(r'^[A-Za-z0-9\s]+$', message):
            raise forms.ValidationError('Message must contain only letters, digits and spaces')
        if not re.match(r'^[A-Za-z0-9\s]+$', description):
            raise forms.ValidationError('Description must contain only letters, digits and spaces')
        if discount is None or discount < 0:
            raise forms.ValidationError('Discount must be a positive number')
        if start_date > end_date:
            raise forms.ValidationError('Start date must be before end date')
        if not combined_choices:
            raise forms.ValidationError('At least one category or dealer must be selected')
        
        return cleaned_data