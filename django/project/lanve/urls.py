from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'lanve'

urlpatterns = [
    path('', views.WelcomeView.as_view(), name='welcome'),
    path('signup/', views.SignupView.as_view(template_name='signup.html'), name='signup'),
    path('signin/', auth_views.LoginView.as_view(template_name='signin.html'), name='signin'),
    # path('signout/', auth_views.LogoutView.as_view(
    #     template_name='signin.html')
    #      ),
    path('home/', views.ListView.as_view(), name='list'),
]
