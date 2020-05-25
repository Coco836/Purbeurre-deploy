# -*- coding: utf-8 -*-

# Import
from django.test import TestCase
from store.models import Category, Product, Shop

# Create your tests here.


class TestModels(TestCase):
    ''' Class test for the models of the application 'store'.'''

    def test_category_fields(self):
        ''' Test the existence of the category in database.'''
        category = Category()
        category.name = 'Category test name'
        category.save()

        response = Category.objects.get(name=category.name)
        self.assertEqual(response, category)

    def test_category_from_api(self):
        ''' Test the saving of a category with specific method 'from_api'. '''
        category_data = {
                    'name': 'first_category',
                    'id': "some name",
                    'url': 'https://url_cat',
        }

        category = Category.from_api(category_data)
        category.save()
        response = Category.objects.get(name=category_data['name'])
        self.assertEqual(response, category)

    def test_product_fields(self):
        ''' Test the existence of the product in database.'''
        product = Product()
        product.name = 'Product test name'
        product.description = 'Description product'
        product.url = 'https://url.fr'
        product.nutrition_grade = 'a'
        product.favorites = False
        product.save()

        response = Product.objects.get(name=product.name)
        self.assertEqual(response, product)

    def test_product_from_api(self):
        ''' Test the saving of a shop with specific method 'from_api'. '''
        prod_data = {
                    'product_name': 'product',
                    'ingredients_text_fr': 'description_prod',
                    'url': 'https://url_product',
                    'nutrition_grade_fr': 'a',
                    'image_url': 'image-prod'
        }

        product = Product.from_api(prod_data)
        product.save()
        response = Product.objects.get(name=prod_data['product_name'])
        self.assertEqual(response, product)

    def test_shop_fields(self):
        ''' Test the existence of the shop in database.'''
        shop = Shop()
        shop.name = 'Shop name test'
        shop.save()

        response = Shop.objects.get(name=shop.name)
        self.assertEqual(response, shop)

    def test_shop_from_api(self):
        ''' Test the saving of a shop with specific method 'from_api'. '''
        shop_data = {
                    'name': 'shop',
                    'url': 'https://url_shop',
        }

        shop = Shop.from_api(shop_data)
        shop.save()
        response = Shop.objects.get(name=shop_data['name'])
        self.assertEqual(response, shop)
