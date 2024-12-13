from django.test import TestCase
import schedule
import django
import time
import os
from . import models
from django.core.mail import send_mass_mail

# Tasks

def delete_inactives():
    users = models.CustomUser.objects.filter(confirmed_mail = False) # Get users that have not confirmed their email
    users.delete() # Delete the users

def send_newsletter():
    users = models.CustomUser.objects.filter() # Get all users
    thirty_minutes_ago = django.utils.timezone.now() - django.utils.timezone.timedelta(minutes=30) # Get the time 30 minutes ago
    recieving_users = users.filter(date_joined__lt=thirty_minutes_ago) # Get users that joined 30 minutes ago
    
    from_email = 'alex6damian@gmail.com' # Email to send from
    subject = 'Newsletter' # Email subject
    message = 'Hello, thanks for being part of our community. We have some news for you. Check our website for more information.' # Email message
    datatuple = []
    for user in recieving_users: 
        datatuple.append((subject, message, from_email, [user.email]))
    
    send_mass_mail(datatuple, fail_silently=False) # Send the newsletter

def delete_old_discounts():
    discounts = models.Discount.objects.filter(expiration_date__lt=django.utils.timezone.now()) # Get discounts that have expired
    discounts.delete() # Delete the discounts
    
def send_black_friday():
    users = models.CustomUser.objects.all() # Get all users
    promo_code = 'BLACKFRIDAY' # Promotion code
    models.Discount.objects.create(code=promo_code, rate=50, expiration_date=django.utils.timezone.now() + django.utils.timezone.timedelta(hours=12))
    
    from_email = 'alex6damian@gmail.com'
    subject = 'Black Friday Promotion'
    message = 'Hello, we have a promotion for you. Use the code BLACKFRIDAY for a 50% discount in all our products. This code is valid for the next 12 hours.'
    datatuple = []
    for user in users:
        datatuple.append((subject, message, from_email, [user.email]))
    
    send_mass_mail(datatuple, fail_silently=False) # Send the promotion