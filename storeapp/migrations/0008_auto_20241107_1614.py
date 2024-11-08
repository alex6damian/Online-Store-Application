from django.db import migrations, models

def set_default_address(apps, schema_editor):
    Dealer = apps.get_model('storeapp', 'Dealer')
    Dealer.objects.filter(address__isnull=True).update(address='')

class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0007_rename_adress_dealer_address'),
    ]

    operations = [
        migrations.RunPython(set_default_address),
        migrations.AlterField(
            model_name='dealer',
            name='address',
            field=models.CharField(max_length=255, default=None, null=True),
        ),
    ]