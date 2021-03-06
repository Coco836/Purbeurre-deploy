# Generated by Django 3.0.6 on 2020-05-20 14:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, unique=True, verbose_name="category's name")),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name="product's name")),
                ('description', models.TextField(null=True, verbose_name='description')),
                ('url', models.URLField(max_length=900, verbose_name='url')),
                ('nutrition_grade', models.CharField(max_length=5, verbose_name='nutriscore')),
                ('image', models.URLField(max_length=300, null=True, verbose_name='image')),
                ('categories', models.ManyToManyField(related_name='products', to='store.Category')),
                ('users', models.ManyToManyField(related_name='products', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name="shop's name")),
                ('products', models.ManyToManyField(related_name='shops', to='store.Product')),
            ],
        ),
    ]
