# -*- coding: utf-8 -*-

# Import
from django.test import TestCase
from store.models import Category, Product, Shop
from unittest import mock
from io import StringIO
from django.core.management import call_command

# Create your tests here.


class TestCommands(TestCase):
    ''' Class test for Management Command. '''

    @mock.patch('store.api.requests.get')
    def test_init_categories(self, mock_get):
        ''' Test the initialization of categories inside the database. '''
        mock_response = mock.Mock()
        # Mock categories data in api
        expected_api_categories = {
                'tags': [{
                    'known': 1,
                    'name': 'first_category',
                    'id': "some name",
                    'url': 'https://url_cat',
                    'products': 1
                }, {
                    'known': 2,
                    'name': 'second_category',
                    'id': "some other name",
                    'url': 'https://url_cat2',
                    'products': 1
                }]
        }
        mock_response.json.return_value = expected_api_categories
        mock_get.return_value = mock_response
        # Write command result in str
        out = StringIO()
        # Call command
        call_command('init_categories', stdout=out)
        self.assertEqual(Category.objects.all().count(), 2)

    @mock.patch('store.api.requests.get')
    def test_init_products(self, mock_get):
        ''' Test the initialization of categories inside the database. '''
        mock_responses = [mock.Mock(), mock.Mock()]
        # Mock categories and products data in api
        expected_api_categories = {
            'tags': [{
                    'known': 1,
                    'name': 'first_category',
                    'id': "some name",
                    'url': 'https://url_cat',
                    'products': 1
                }]
        }
        expected_api_products = {
                'products': [{
                    'product_name': 'aliment',
                    'ingredients_text_fr': 'ingredient',
                    'url': "https://url_prod",
                    'image_url': 'https://image_url_product',
                    'nutrition_grade_fr': 'a',
                    'categories': 'first_category',
                    'stores': 'Carrefour, Magasin U'
                }]
        }
        mock_responses[0].json.return_value = expected_api_categories
        mock_responses[1].json.return_value = expected_api_products
        mock_get.side_effect = mock_responses
        out = StringIO()
        call_command('init_products', stdout=out)

        self.assertEqual(Category.objects.all().count(), 1)
        self.assertEqual(Product.objects.all().count(), 1)
        self.assertEqual(Shop.objects.all().count(), 2)
        self.assertEqual(Product.categories.through.objects.all().count(), 1)
