# Generated by Django 3.1.7 on 2021-03-31 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20210331_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='SubcatName',
            field=models.ManyToManyField(blank=True, related_name='subcat', to='home.subcategory', verbose_name='Sub-category Name'),
        ),
    ]
