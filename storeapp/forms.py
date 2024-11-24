from django import forms
from django.db import models
from .models import Dealer, Category, Product, CustomUser
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

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=10, required=True, label = 'First Name')
    second_name = forms.CharField(max_length=15, required=False, label = 'Second Name')
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
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
    message_type = forms.ChoiceField(choices=message_type_choises, required=False, label = 'Message Type')
    subject = forms.CharField(max_length=15, required=True, label = 'Subject')
    waiting_time = forms.IntegerField(required=False, label = 'Waiting Time')
    message = forms.CharField(widget=forms.Textarea, required = False, label = 'Message') 

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
        fields = ['name', 'price', 'stock', 'category', 'dealer']
        labels = {
            'name': 'Product Name',
            'price': 'Price ($)',
            'stock': 'Stock',
            'category' : 'Category',
            'dealer' : 'Dealer',
            }
        help_texts = {
            'name': 'Enter the product name. Only letters and spaces are allowed.',
            'price': 'Enter the price of the product. Must be a positive number.',
            'stock': 'Enter the stock quantity. Must be a positive number.',
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
            'bio': forms.Textarea(attrs={'required': False}),
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