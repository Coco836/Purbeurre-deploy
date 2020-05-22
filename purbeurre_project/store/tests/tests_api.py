# -*- coding: utf-8 -*-

# Import
from django.test import TestCase
from store.models import Category
from unittest import mock
from store.api import OpenFoodFactsApi

# Create your tests here.


class TestApi(TestCase):
    ''' Class test for OpenFoodFacts API. '''

    @mock.patch('store.api.requests.get')
    def test_fetch_stores_data_api(self, mock_get):
        ''' Test the recovery of stores data from api. '''
        mock_response = mock.Mock()
        # Mock stores data in api
        expected_api_stores = {
                'tags': [{
                    'known': 1,
                    'name': 'first_store',
                    'id': "some name",
                    'url': 'https://url_store',
                    'products': 1
                }]
        }
        mock_response.json.return_value = expected_api_stores
        mock_get.return_value = mock_response
        response = OpenFoodFactsApi().fetch_stores_data_api()
        self.assertEqual(response, expected_api_stores['tags'])
        # Making sure the right url was called
        mock_get.assert_called_once_with(
                        "https://fr.openfoodfacts.org/categorie/stores.json"
        )

    @mock.patch('store.api.requests.get')
    def test_fetch_categories_data_api(self, mock_get):
        ''' Test the recovery of categories data from api. '''
        mock_response = mock.Mock()
        # Mock categories data in api
        expected_api_categories = {
                'tags': [{
                    'known': 1,
                    'name': 'first_category',
                    'id': "some name",
                    'url': 'https://url_cat',
                    'products': 1
                }]
        }
        mock_response.json.return_value = expected_api_categories
        mock_get.return_value = mock_response
        response = OpenFoodFactsApi().fetch_categories_data_api()
        self.assertEqual(response, expected_api_categories['tags'])
        # Making sure the right url was called
        mock_get.assert_called_once_with(
                                "https://fr.openfoodfacts.org/categories.json"
        )

    @mock.patch('store.api.requests.get')
    def test_fetch_products_data_api(self, mock_get):
        ''' Test the recovery of products data from api. '''
        category = Category()
        category.name = 'Category test name'
        category.save()

        mock_response = mock.Mock()
        # Mock products data in api
        expected_api_products = {
                'products': [{
                    'product_name': 'aliment',
                    'ingredients_test_fr': 'ingredient',
                    'url': "https://url_prod",
                    'image_url': 'https://image_url_product',
                }]
        }
        mock_response.json.return_value = expected_api_products
        mock_get.return_value = mock_response
        response = OpenFoodFactsApi().fetch_products_data_api(category)
        self.assertEqual(response, expected_api_products['products'])
        # Making sure the right url was called
        mock_get.assert_called_once_with(
                f'''https://fr.openfoodfacts.org/categorie/{category}.json'''
        )
