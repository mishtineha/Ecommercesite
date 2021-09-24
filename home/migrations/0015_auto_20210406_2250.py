# Generated by Django 3.1.7 on 2021-04-06 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20210402_0045'),
    ]

    operations = [
        migrations.CreateModel(
            name='topsale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=500, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topsale_product', to='home.product', verbose_name='Product')),
            ],
        ),
        migrations.DeleteModel(
            name='newrelease',
        ),
    ]
