# Generated by Django 3.1.7 on 2021-03-11 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('home', '0004_auto_20210311_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_images',
            name='image1',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_image1', to=settings.FILER_IMAGE_MODEL, verbose_name='image1(1860 x 1860)'),
        ),
        migrations.AlterField(
            model_name='product_images',
            name='image2',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_image2', to=settings.FILER_IMAGE_MODEL, verbose_name='image2(1860 x 1860)'),
        ),
        migrations.AlterField(
            model_name='product_images',
            name='image3',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_image3', to=settings.FILER_IMAGE_MODEL, verbose_name='image3(1860 x 1860)'),
        ),
        migrations.AlterField(
            model_name='product_images',
            name='image4',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_image4', to=settings.FILER_IMAGE_MODEL, verbose_name='image4(1860 x 1860)'),
        ),
        migrations.AlterField(
            model_name='product_images',
            name='name',
            field=models.CharField(default='Sayra', max_length=200, verbose_name='Product Name'),
        ),
    ]
