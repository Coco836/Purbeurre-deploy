# Import
from django.test import TestCase, Client
from django.urls import reverse
from store.models import Product
from django.contrib.auth.models import User


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
            User.objects.get(username='someusername')
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
        # Check if the user n°6 is currently logged in
        self.assertEqual('6', self.client.session.get('_auth_user_id'))
        response = self.client.get('/account/logout/?next=/')
        self.assertEqual(response.status_code, 302)
        # Check if the user n°6 is currently logged out
        self.assertNotEqual('6', self.client.session.get('_auth_user_id'))

    def test_saved_food(self):
        ''' Test if the products saved as favorite exist in database. '''
        User.objects.create_user(**self.data)
        self.client.login(
                                    username=self.login_data['username'],
                                    password=self.login_data['password']
        )
        user = User.objects.get(username=self.login_data['username'])
        substitute = Product.objects.create(**self.data_product)
        substitute.users.add(user)
        response = self.client.get(reverse('saved_food'))
        self.assertEqual(User.products.through.objects.all().count(), 1)
        self.assertTemplateUsed(response, 'account/saved_food.html')
