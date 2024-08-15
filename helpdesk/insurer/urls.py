from django.urls import path
from . import views
app_name='insurer'
urlpatterns = [
    path("",views.insurer,name='insurer'),
    path("user/",views.show_users,name='show_users'),
    path("claims/",views.show_claims,name='show_claims'),
    path("filter_userid/",views.filter_userid,name="filter_userid"),
    path("filter_policy_name/",views.filter_policy_name,name="filter_policy_name"),
    path("filter_userid_claims/",views.filter_userid_claims,name="filter_userid_claims"),
    path("filter_policy_name_claims/",views.filter_policy_name_claims,name="filter_policy_name_claims")
    
]