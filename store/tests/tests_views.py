# -*- coding: utf-8 -*-

# Import
from django.test import TestCase, Client
from django.urls import reverse
from store.models import Category, Product
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
