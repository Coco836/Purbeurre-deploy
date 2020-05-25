# Import
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from purbeurre_project.store.models import Product
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout


# Create your views here.
def index(request):
    ''' View that send user to homepage of the website. '''
    template = loader.get_template('store/index.html')
    return HttpResponse(template.render(request=request))


def sign_up(request):
    ''' View allowing users to sign-up in the website. '''
    # Send the form to the template
    context = {
                'form': UserForm,
            }
    # If the user try to sign-up, send new form with the request.
    if request.method == 'POST':
        form = UserForm(request.POST)
        context = {
            'form': form,
        }

        if form.is_valid():
            # Create the user and save it in database
            new_user = User.objects.create_user(
                username=form.cleaned_data['username'],
                last_name=form.cleaned_data['last_name'],
                first_name=form.cleaned_data['first_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            new_user.save()

            return render(request, 'account/valid_sign_up.html')
        return render(request, 'registration/sign_up.html', context)

    return render(request, 'registration/sign_up.html', context)


def login_view(request):
    '''
        View allowing user to login in the website
        and to access more functionalities.
    '''
    # Send the form to the template
    context = {
            'form': UserForm,
        }
    # If the user try to login, send new form with the request.
    if request.method == 'POST':
        form = UserForm(request.POST)
        context = {
            'form': form,
        }
        # Retrieve data entered by the user
        user = authenticate(
                            request,
                            username=request.POST['username'],
                            password=request.POST['password']
        )
        # Send back the user to the current page if the data are not valid
        if user is None:
            return render(request, 'registration/login.html', context)
        # Login user if the data are valid
        login(request, user)
        return render(request, 'account/my_account.html')

    return render(request, 'registration/login.html', context)


@login_required
def logout_view(request):
    ''' View allowing user to logout of the website. '''
    # Send request
    logout(request)
    return redirect('/')


@login_required
def my_account(request):
    ''' View that render template. '''
    return render(request, 'account/my_account.html')


@login_required
def saved_food(request):
    ''' View that send saved product data to template. '''
    # Retrieve current user
    user = request.user
    # Only retrieve favorite product linked to the current user
    substitutes_saved = User.products.through.objects.filter(user_id=user)
    # Create list of favorite substitute from current user
    list_saved_substitutes = []
    for subs in substitutes_saved:
        saved_subs = Product.objects.filter(id=subs.product_id)
        list_saved_substitutes.append(saved_subs)
    # Send data to template
    context = {
        'list_saved_substitutes': list_saved_substitutes
    }
    return render(request, 'account/saved_food.html', context)
