# Import
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    ''' Create model for Categories. '''
    name = models.CharField(
                            "category's name",
                            max_length=500,
                            null=False,
                            unique=True
    )

    @classmethod
    def from_api(cls, json_category):
        ''' Method allowing creation of a category. '''
        return cls(name=json_category['name'])

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    ''' Create model for Products. '''
    name = models.CharField(
                            "product's name",
                            max_length=200,
                            null=False,
                            unique=True
    )
    description = models.TextField('description', null=True)
    url = models.URLField('url', max_length=900, null=False)
    nutrition_grade = models.CharField('nutriscore', max_length=5)
    image = models.URLField('image', max_length=300, null=True)
    # Create many to many field to link a product to its categories
    categories = models.ManyToManyField(Category, related_name='products')
    # Create many to many field to link a product to a user
    users = models.ManyToManyField(User, related_name='products')

    @classmethod
    def from_api(cls, json_product):
        ''' Method allowing creation of a product. '''
        return cls(
                    name=json_product['product_name'],
                    description=json_product['ingredients_text_fr'],
                    url=json_product['url'],
                    nutrition_grade=json_product['nutrition_grade_fr'],
                    image=json_product['image_url'],
        )

    def __str__(self):
        return f'{self.name}'


class Shop(models.Model):
    ''' Create model for Stores. '''
    name = models.CharField("shop's name", max_length=200, null=False)
    # Create many to many field to link product to shops where it can be found
    products = models.ManyToManyField(Product, related_name='shops')

    @classmethod
    def from_api(cls, json_shop):
        ''' Method allowing creation of a shop. '''
        return cls(name=json_shop['name'])

    def __str__(self):
        return f'{self.name}'
