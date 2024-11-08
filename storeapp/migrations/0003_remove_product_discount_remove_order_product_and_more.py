# Generated by Django 5.1.1 on 2024-11-07 13:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0002_order_product_delete_productorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('product_order_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_price', models.FloatField()),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='storeapp.discount')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storeapp.order')),
                ('product', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='storeapp.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='storeapp.product'),
            preserve_default=False,
        ),
    ]
