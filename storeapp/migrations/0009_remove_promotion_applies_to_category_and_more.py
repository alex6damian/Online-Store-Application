# Generated by Django 5.1.3 on 2024-12-07 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0008_remove_promotion_applies_to_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promotion',
            name='applies_to_category',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='applies_to_dealer',
        ),
    ]