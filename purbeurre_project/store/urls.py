from django.urls import path, include
from . import views # import views so we can use them in urls.


urlpatterns = [
    path(r'search/', views.search, name='search'),
    path(r'product_categories/<int:product_id>/', views.product_categories, name='product_categories'),
    path(r'listing_substitutes/<int:product_id>/<int:category_id>/', views.listing_substitutes, name='listing_substitutes'),
    path(r'substitute_details/<str:substitute_name>/', views.substitute_details, name='substitute_details'),
    path(r'favorite/<int:substitute_id>/', views.save_product, name='favorite'),
    path(r'delete/<int:substitute_id>/', views.delete_substitute, name='favorite_delete'),
    path(r'mention/', views.mention, name='mention')

]