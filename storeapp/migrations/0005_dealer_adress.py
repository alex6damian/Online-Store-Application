# Generated by Django 5.1.1 on 2024-11-07 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0004_product_order_remove_order_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealer',
            name='adress',
            field=models.CharField(default=None, max_length=255),
        ),
    ]