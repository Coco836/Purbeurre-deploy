# Import
from django.test import TestCase, Client
from django.urls import reverse
from account.forms import UserForm
from account import forms
from django.core.exceptions import ValidationError
from store.models import Product, Category
from django.contrib.auth.hashers import (
                                        make_password,
                                        is_password_usable,
                                        check_password
)
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
# Selenium
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


# Create your tests here.


class TestViews(TestCase):
    ''' Class test for the views of the application 'account' '''

    def setUp(self):
        '''
            Create test records once to access them in
            every test method in the test class.
        '''
        self.client = Client()
        self.home_url = reverse('home')
        self.account_url = reverse('my_account')
        self.sign_up_url = reverse('sign_up')
        self.login_url = reverse('login')
        self.favorite_url = reverse('saved_food')
        self.data = {
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
        self.data_product = {
            'name': 'nutella',
            'description': 'product_description',
            'url': 'https://url',
            'nutrition_grade': 'd',
            'image': 'https://image',
        }

    def test_sign_up_get(self):
        ''' Test that sign-up form appears in template. '''
        response = self.client.get(self.sign_up_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/sign_up.html')
        self.assertContains(response, 'Inscription')
        self.assertContains(
                            response,
                            '''<input type="text" name="username" '''
                            '''class="form-group"'''
        )

    def test_sign_up_post_success(self):
        ''' Test that sign-up form was successfully filled by user. '''
        response = self.client.post(self.sign_up_url, self.data)
        self.assertTemplateUsed(response, 'account/valid_sign_up.html')
        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.filter(username=self.data['username'])
        for user in new_user:
            self.assertEqual(user.username, 'fred')

    def test_login_get(self):
        ''' Test that login form appears clearly in template. '''
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Connexion')
        self.assertContains(
                            response,
                            '''<input type="password" '''
                            '''name="password" class="form-group"'''
        )

    def test_login_success(self):
        ''' Test that login form was successfully filled by user. '''
        User.objects.create_user(**self.data)
        response = self.client.post(self.login_url, self.login_data)
        self.assertTemplateUsed(response, 'account/my_account.html')
        self.assertContains(response, self.data['email'])
        self.assertContains(response, '''<a class="deconnection" ''')

    def test_my_account(self):
        '''
            Test that template 'my_account' appears 
            when the user has successfully logged in.
        '''
        User.objects.create_user(**self.data)
        self.client.post(self.login_url, self.login_data)
        response = self.client.get(self.account_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/my_account.html')
        self.assertContains(response, "Bonjour")
        self.assertContains(response, '''<a class="deconnection" ''')

    def test_login_fail(self):
        ''' Test that user stay in the same template when login failed. '''
        User.objects.create_user(**self.data)
        response = self.client.post(
                                    self.login_url,
                                    {
                                        'username': 'someusername',
                                        'password': 'somepassword'
                                    }
        )
        try:
            user = User.objects.get(username='someusername')
        except User.DoesNotExist:
            self.assertRaises(User.DoesNotExist)
            self.assertTemplateUsed(response, 'registration/login.html')
            self.assertContains(
                                response,
                                "Le nom d'utilisateur et le mot de passe"
                                " ne correspondent pas !"
            )

    def test_logout_view(self):
        ''' Test that client session is clear when the user logout. '''
        User.objects.create_user(**self.data)
        self.client.login(
                            username=self.login_data['username'],
                            password=self.login_data['password']
        )
        user = User.objects.get(username=self.login_data['username'])
        # Check if the user n°6 is currently logged in
        self.assertEqual('6', self.client.session.get('_auth_user_id'))
        response = self.client.get('/account/logout/?next=/')
        self.assertEqual(response.status_code, 302)
        # Check if the user n°6 is currently logged out
        self.assertNotEqual('6', self.client.session.get('_auth_user_id'))

    def test_saved_food(self):
        ''' Test if the products saved as favorite exist in database. '''
        User.objects.create_user(**self.data)
        request = self.client.login(
                                    username=self.login_data['username'],
                                    password=self.login_data['password']
        )
        user = User.objects.get(username=self.login_data['username'])
        substitute = Product.objects.create(**self.data_product)
        substitute.users.add(user)
        response = self.client.get(reverse('saved_food'))
        self.assertEqual(User.products.through.objects.all().count(), 1)
        self.assertTemplateUsed(response, 'account/saved_food.html')


class TestForms(TestCase):
    ''' Class test for the form in of the application 'account'.'''

    def setUp(self):
        '''
            Create test records once to access them in
            every test method in the test class.
        '''
        self.client = Client()
        self.data = {
                     'username': 'fred',
                     'last_name': 'Sacquet',
                     'first_name': 'Frodon',
                     'email': 'frodon@sacquet.fr',
                     'password': 'test',
        }

    def test_user_form_valid_data(self):
        ''' Test the validity of the data entered by the user.'''
        form = UserForm(self.data)
        self.assertTrue(form.is_valid())

    def test_user_form_no_data(self):
        ''' Test the non validity of the data entered by the user.'''
        form = UserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)

    def test_email_is_unique(self):
        ''' Test validity of the email when user try to sign-up. '''
        self.client.post(reverse('sign_up'), self.data)
        response = self.client.post(reverse('sign_up'), self.data)
        # Check if error appears as it should
        self.assertContains(response, 'Cette adresse email existe déjà !')

    def test_username_is_unique(self):
        ''' Test validity of the username when user try to sign-up. '''
        self.client.post(reverse('sign_up'), self.data)
        response = self.client.post(reverse('sign_up'), self.data)
        # Check if error appears as it should
        self.assertContains(response, 'utilisateur existe déjà')


class TestModels(TestCase):
    ''' Class test for the django model User of the application 'account'.'''

    def setUp(self):
        '''
            Create test records once to access them in
            every test method in the test class.
        '''
        self.data = {
                    'id': 1,
                    'username': 'fred',
                    'last_name': 'Sacquet',
                    'first_name': 'Frodon',
                    'email': 'frodon@sacquet.fr',
                    'password': 'test',
        }

    def test_user_fields(self):
        ''' Test the existence of the user in database.'''
        user = User()
        user.username = "Username test"
        user.last_name = "Last name test"
        user.first_name = "First name test"
        user.email = "Email@test.fr"
        user.password = "Password test"
        user.save()

        response = User.objects.get(email=user.email)
        self.assertEqual(response, user)


class MySeleniumTests(StaticLiveServerTestCase):

    def setUp(self):
        self.data_product = {
            'name': 'nutella',
            'description': 'product_description',
            'url': 'https://url',
            'nutrition_grade': 'd',
            'image': 'https://image',
        }
        self.data_substitute = {
            'name': 'chocolat',
            'description': 'product_description',
            'url': 'https://url',
            'nutrition_grade': 'a',
            'image': 'https://image',
        }
        self.data_category = {
            'name': 'pâte à tartiner'
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

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_1_signup_and_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, reverse('sign_up')))
        self.selenium.find_element_by_name("username").send_keys('Test')
        self.selenium.find_element_by_name("last_name").send_keys('testname')
        self.selenium.find_element_by_name("first_name").send_keys('test')
        self.selenium.find_element_by_name("email").send_keys(
                                                        'emailtest@email.fr'
                                                        )
        self.selenium.find_element_by_name("password").send_keys('pass')
        self.selenium.find_element_by_xpath(
                                            '''//input[@value="S'inscrire"]'''
                                            ).click()
        self.selenium.find_element_by_class_name("connection-link").click()
        self.selenium.find_element_by_name("username").send_keys('Test')
        self.selenium.find_element_by_name("password").send_keys('pass')
        self.selenium.find_element_by_xpath(
                                            '//input[@value="Se connecter"]'
                                            ).click()

    def test_2_search(self):
        Product.objects.create(**self.data_product)
        self.selenium.get('%s%s' % (self.live_server_url, reverse('home')))
        self.selenium.find_element_by_id("product").send_keys('nutella')
        self.selenium.find_element_by_id('btn-accueil').click()
    
    def test_3_add_favorite(self):
        # Sign-up and log-in user
        self.selenium.get('%s%s' % (self.live_server_url, reverse('sign_up')))
        self.selenium.find_element_by_name("username").send_keys('Test')
        self.selenium.find_element_by_name("last_name").send_keys('testname')
        self.selenium.find_element_by_name("first_name").send_keys('test')
        self.selenium.find_element_by_name("email").send_keys(
                                                        'emailtest@email.fr'
                                                        )
        self.selenium.find_element_by_name("password").send_keys('pass')
        self.selenium.find_element_by_xpath(
                                            '''//input[@value="S'inscrire"]'''
                                        ).click()
        self.selenium.find_element_by_class_name("connection-link").click()
        self.selenium.find_element_by_name("username").send_keys('Test')
        self.selenium.find_element_by_name("password").send_keys('pass')
        self.selenium.find_element_by_xpath(
                                            '//input[@value="Se connecter"]'
                                            ).click()

        # Create products, category and add link to them
        product = Product.objects.create(**self.data_product)
        category = Category.objects.create(**self.data_category)
        substitute = Product.objects.create(**self.data_substitute)
        product.categories.add(category)
        substitute.categories.add(category)

        # Add substitute as favorite
        self.selenium.get('%s%s' % (self.live_server_url, reverse('home')))
        self.selenium.find_element_by_id("product").send_keys('nutella')
        self.selenium.find_element_by_id('btn-accueil').click()
        self.selenium.find_element_by_id("prod-name").click()
        self.selenium.find_elements_by_id("category-search")[0].click()
        self.selenium.find_element_by_name("button-save").click()
        self.selenium.get('%s%s' % (self.live_server_url, reverse('saved_food')))




        # self.selenium.get('%s%s' % (self.live_server_url, reverse('sign_up')))
        # self.selenium.find_element_by_name("username").send_keys('Test')
        # self.selenium.find_element_by_name("last_name").send_keys('testname')
        # self.selenium.find_element_by_name("first_name").send_keys('test')
        # self.selenium.find_element_by_name("email").send_keys('emailtest@email.fr')
        # self.selenium.find_element_by_name("password").send_keys('pass')
        # self.selenium.find_element_by_xpath('''//input[@value="S'inscrire"]''').click()
        # self.selenium.find_element_by_class_name("connection-link").click()
        # self.selenium.find_element_by_name("username").send_keys('Test')
        # self.selenium.find_element_by_name("password").send_keys('pass')
        # self.selenium.find_element_by_xpath('//input[@value="Se connecter"]').click()





