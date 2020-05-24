from django.urls import path
from . import views


urlpatterns = [
    path(r'sign_up/', views.sign_up, name='sign_up'),
    path(r'login/', views.login_view, name='login'),
    path(r'logout/', views.logout_view, name='logout'),
    path(r'my_account/', views.my_account, name='my_account'),
    path(r'saved_food/', views.saved_food, name='saved_food')
]
