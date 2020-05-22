# -*- coding: utf-8 -*-

# Import
from django.test import TestCase, Client
from django.urls import reverse
from store.models import Category, Product, Shop
from unittest import mock
from io import StringIO
from django.core.management import call_command
from store.api import OpenFoodFactsApi
from django.contrib.auth.models import User

# Create your tests here.


class TestViews(TestCase):
    ''' Class test for the views of the application 'store' '''

    def setUp(self):
        '''
            Create test records once to access them in
            every test method in the test class.
        '''
        self.client = Client()
        self.home_url = reverse('home')
        self.search_url = reverse('search')
        self.login_url = reverse('login')
        self.data_product = {
            'name': 'nutella',
            'description': 'product_description',
            'url': 'https://url',
            'nutrition_grade': 'd',
            'image': 'https://image',
        }
        self.data_substitute = {
            'name': 'substitute_name',
            'description': 'substitute_description',
            'url': 'https://url_subs',
            'nutrition_grade': 'a',
            'image': 'https://image_subs',
        }
        self.data_category = {
            'name': 'category'
        }
        self.user_data = {
                'username': 'fred',
                'last_name': 'Sacquet',
                'first_name': 'Frodon',
                'email': 'frodon@sacquet.fr',
                'password': 'test',
        }
        self.login_data = {
            'username': 'fred',
            'password': 'test'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_index(self):
        ''' Test if homepage is well displayed'''
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/index.html')
        self.assertContains(response, "Du gras, oui, mais de qualité !")

    def test_search_exist(self):
        ''' Test search functionality with existing value.'''
        name = 0
        # Create products
        for i in range(15):
            Product.objects.create(
                                    name=f"nutella{name}",
                                    description="desc",
                                    url="url",
                                    nutrition_grade="nutri",
                                    image="image"
            )
            name += 1
        # Create user input
        user_input = 'nut'
        # Send user input to search form
        response = self.client.get(
                                    self.search_url,
                                    data={'user_input': user_input}
        )
        self.assertIn(user_input, response.content.decode())
        self.assertTemplateUsed(response, "store/search.html")

    def test_search_empty_page(self):
        ''' Test search functionality with non existing value for user input'''
        name = 0
        # Create products
        for i in range(15):
            Product.objects.create(
                                    name=f"nutella{name}",
                                    description="desc",
                                    url="url",
                                    nutrition_grade="nutri",
                                    image="image"
            )
            name += 1
        # Create empty user input
        user_input = ''
        # Send user input to search form
        response = self.client.get(
                                    self.search_url,
                                    data={'user_input': user_input}
        )
        self.assertIn(user_input, response.content.decode())
        self.assertTemplateUsed(response, "store/index.html")

    def test_product_categories(self):
        ''' Test link bewteen a product and its categories. '''
        product = Product.objects.create(**self.data_product)
        category = Category.objects.create(**self.data_category)
        # Add link between a product and a category
        product.categories.add(category)
        response = self.client.get(
                                    reverse(
                                            'product_categories',
                                            args=[product.id]
                                    )
        )
        link_cat_prod = product.categories.all()
        for link in link_cat_prod:
            self.assertContains(response, link)
            self.assertEquals(response.status_code, 200)

    def test_listing_substitutes(self):
        ''' Test the listing of substitutes in template. '''
        product = Product.objects.create(**self.data_product)
        category = Category.objects.create(**self.data_category)
        substitute = Product.objects.get(id=product.id)
        category_subs = Category.objects.get(id=category.id)
        # Add link between a product and a category
        substitute.categories.add(category_subs)
        response = self.client.get(
                                    reverse(
                                            'listing_substitutes',
                                            args=[product.id, category.id]
                                    )
        )
        self.assertEqual(Product.categories.through.objects.all().count(), 1)
        self.assertTemplateUsed(response, 'store/listing_substitutes.html')

    def test_substitute_details(self):
        ''' Test the substitutes details in template. '''
        product = Product.objects.create(**self.data_product)
        substitute = Product.objects.create(**self.data_substitute)
        category = Category.objects.create(**self.data_category)
        product.categories.add(category)
        substitute.categories.add(category)
        product_substitutes = (
                                category.products.filter(
                                    nutrition_grade__lt=product.nutrition_grade
                                ).order_by("-nutrition_grade")[:9]
        )
        for subs in product_substitutes:
            response = self.client.get(
                                        reverse(
                                                'substitute_details',
                                                args=[subs.name]
                                        )
            )
            self.assertContains(response, subs)
            self.assertEquals(response.status_code, 200)

    def test_save_product(self):
        ''' Test the save as favorite functionality. '''
        # User has to be login
        self.client.login(
                                    username=self.login_data['username'],
                                    password=self.login_data['password']
        )
        substitute = Product.objects.create(**self.data_product)
        category = Category.objects.create(**self.data_category)
        substitute.categories.add(category)
        # Add the link between a user and the product he saved
        response = self.client.post(
                                    reverse(
                                            'favorite',
                                            args=[substitute.id]
                                    ),
                                    HTTP_REFERER=reverse(
                                            'listing_substitutes',
                                            args=[substitute.id, category.id]
                                    ),
        )
        self.assertEqual(User.products.through.objects.all().count(), 1)
        self.assertRedirects(
                            response,
                            '/store/listing_substitutes/'
                            f'{substitute.id}/{category.id}/'
        )

    def test_delete_substitute(self):
        ''' Test the delete favorite functionality. '''
        # User has to be login
        self.client.login(
                                    username=self.login_data['username'],
                                    password=self.login_data['password']
        )
        substitute = Product.objects.create(**self.data_product)
        substitute.users.add(self.user)
        self.assertEqual(User.products.through.objects.all().count(), 1)
        # Remove the link of the user with the choosen product
        response = self.client.post(
                                    reverse(
                                            'favorite_delete',
                                            args=[substitute.id]
                                    ),
                                    HTTP_REFERER=reverse(
                                            'saved_food'
                                    ),
        )
        self.assertEqual(User.products.through.objects.all().count(), 0)
        self.assertRedirects(response, '/account/saved_food/')

    def test_mention(self):
        ''' Test if mention page is well displayed'''
        response = self.client.get(reverse('mention'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/mention.html')
        self.assertContains(response, "Mentions légales")


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
