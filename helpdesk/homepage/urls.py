from django.urls import path
from . import views


urlpatterns = [
    path("",views.index,name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('homepage/', views.home, name='home'),
    path('network_hospitals/', views.network_hospitals, name='network_hospitals'),
    path('filter_hospitals/', views.filter_hospitals, name='filter_hospitals'),
]