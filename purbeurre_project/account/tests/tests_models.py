# Import
from django.test import TestCase
from django.contrib.auth.models import User


# Create your tests here.


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
