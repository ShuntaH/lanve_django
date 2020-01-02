from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'lanve'

urlpatterns = [
    path('', views.WelcomeView.as_view(), name='welcome'),
    path(r'signup/', views.SignupView.as_view(template_name='signup.html'), name='signup'),
    path(r'signin/', auth_views.LoginView.as_view(template_name='signin.html'), name='signin'),
    # path('signout/', auth_views.LogoutView.as_view(
    #     template_name='signin.html')
    #      ),
    path(r'home/', views.ListView.as_view(), name='list'),
    path(r'add/', views.AddView.as_view(), name='add'),
]
