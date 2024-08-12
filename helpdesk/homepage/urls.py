from django.urls import path
from . import views

app_name="homepage"
urlpatterns = [
    path("",views.index,name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('homepage/', views.home, name='home'),
    path('network_hospitals/', views.network_hospitals, name='network_hospitals'),
    path('filter_hospitals/', views.filter_hospitals, name='filter_hospitals'),
    path('create_claim/', views.create_claim, name='create_claim'),
    path('delete_claim/<int:claim_id>/', views.delete_claim, name='delete_claim'),
    path('renew/',views.renew, name='renew'),
    path('logout/', views.custom_logout, name='logout'),
]