# Import
from django.test import TestCase, Client
from django.urls import reverse
from account.forms import UserForm


# Create your tests here.


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
