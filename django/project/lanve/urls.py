from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'lanve'

urlpatterns = [
    path('', views.WelcomeView.as_view(), name='welcome'),
    path(r'signup/', views.SignupView.as_view(template_name='signup.html'), name='signup'),
    path(r'signin/', auth_views.LoginView.as_view(template_name='signin.html'), name='signin'),
    path('signout/', auth_views.LogoutView.as_view(template_name='signout.html'), name='signout'),
    path(r'home/', views.ListView.as_view(), name='list'),
    path(r'add/', views.AddView.as_view(), name='add'),
    path(r'detail/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path(r'mypage/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path(r'mypage/update/<int:pk>', views.UserUpdateView.as_view(), name='user_form'),
    path('password_change/', views.MyPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.MyPasswordChangeDoneVIew.as_view(), name='password_change_done'),
    path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
