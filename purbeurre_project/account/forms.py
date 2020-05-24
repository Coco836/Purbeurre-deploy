# Import
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class UserForm(forms.Form):
    ''' Form sign-up for new user. '''

    def email_is_unique(email):
        '''
            Method that raises error if the email
            entered by the user already exists.
        '''
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            raise ValidationError('Cette adresse email existe déjà !')

    def username_is_unique(username):
        '''
            Method that raises error if the username
            entered by the user already exists.
         '''
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        else:
            raise ValidationError(" Ce nom d'utilisateur existe déjà !")

    # Creation of the different fields for User table
    username = forms.CharField(
            label='username',
            max_length=100,
            widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-group',
                                        'type': 'text',
                                        'name': 'username',
                                        'id': 'user-name',
                                        'placeholder': "Nom d'utilisateur"
                                    }
            ),
            validators=[username_is_unique],
            required=True
    )
    last_name = forms.CharField(
            label='lastname',
            max_length=200,
            widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-group',
                                        'type': 'text',
                                        'name': 'lastname',
                                        'id': 'last-name',
                                        'placeholder': 'Nom'
                                    }
            ),
            required=True
    )
    first_name = forms.CharField(
            label='firstname',
            max_length=200,
            widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-group',
                                        'type': "text",
                                        'name': 'firstname',
                                        'id': 'first-name',
                                        'placeholder': 'Prénom'}),
            required=True
    )
    email = forms.EmailField(
            label='email',
            max_length=100,
            widget=forms.EmailInput(
                                    attrs={
                                        'class': 'form-group',
                                        'type': "email",
                                        'name': 'email',
                                        'id': 'email',
                                        'placeholder': 'Adresse mail'
                                    }
            ),
            validators=[email_is_unique],
            required=True
    )
    password = forms.CharField(
            label='pass',
            max_length=100,
            widget=forms.PasswordInput(
                                        attrs={
                                            'class': 'form-group',
                                            'type': "password",
                                            'name': 'pass',
                                            'id': 'pass',
                                            'placeholder': 'Mot de passe'
                                        }
            ),
            required=True

    )
