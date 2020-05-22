# Import
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger('Pur Beurre')


# Create your views here.
def index(request):
    ''' View that send user to homepage of the website. '''
    template = loader.get_template('store/index.html')
    return HttpResponse(template.render(request=request))


def search(request):
    ''' View that send associated results of user research. '''
    user_input_query = request.GET.get('user_input')
    query_set = Product.objects.all()

    if user_input_query != '' and user_input_query is not None:
        # Search for products containing the user input in database
        query_set = query_set.filter(name__icontains=user_input_query)
        # Set maximum number of products per page
        paginator = Paginator(query_set, 9)
        # Set page number when PageIsNotAnInteger
        try:
            page = int(request.GET.get('page'))
        except Exception:
            page = 1
        # Send to last page with products when next page is Empty
        try:
            products = paginator.page(page)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context = {
            'user_input': user_input_query,
            'products': products,
            'paginate': True
        }
        return render(request, 'store/search.html', context)

    return render(request, 'store/index.html')


def product_categories(request, product_id):
    ''' View that send associated categories of products in search result. '''
    product = Product.objects.get(pk=product_id)
    categories = product.categories.all()
    context = {
        'categories': categories,
        'product': product
    }
    return render(request, 'store/product_categories.html', context)


def listing_substitutes(request, product_id, category_id):
    ''' View that send substitutes for product in the choosen category. '''
    product = Product.objects.get(pk=product_id)
    category = Category.objects.get(pk=category_id)
    # Find substitute with better nutriscore for product
    product_substitutes = (
                            category.products.filter(
                                nutrition_grade__lt=product.nutrition_grade
                            ).order_by("-nutrition_grade")[:9]
    )
    context = {
        'product': product,
        'category': category,
        'product_substitutes': product_substitutes,

    }
    return render(request, 'store/listing_substitutes.html', context)


def substitute_details(request, substitute_name):
    ''' View that send substitute details. '''
    substitute = Product.objects.get(name=substitute_name)
    shops = substitute.shops.all()
    context = {
        'substitute': substitute,
        'shops': shops
    }
    return render(request, 'store/substitute_details.html', context)


@login_required
def save_product(request, substitute_id):
    ''' View that allows a user to save a substitute as favorite. '''
    substitute = Product.objects.get(id=substitute_id)
    user = request.user
    substitute.users.add(user)
    # Redirect to current page
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_substitute(request, substitute_id):
    '''
        View that allows a user to delete
        a substitute in saved_food template.
    '''
    substitute = Product.objects.get(id=substitute_id)
    user = request.user
    substitute.users.remove(user)
    # Redirect to current page
    return redirect(request.META.get('HTTP_REFERER'))


def mention(request):
    ''' View that render template. '''
    return render(request, 'store/mention.html')
