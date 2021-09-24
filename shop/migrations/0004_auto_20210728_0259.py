# Generated by Django 3.1.7 on 2021-07-27 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_auto_20210424_0001'),
        ('shop', '0003_alter_orderitem_variant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicemodel',
            name='address2',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Address Line 2 '),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='wished_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wished_product', to='home.product'),
        ),
    ]
