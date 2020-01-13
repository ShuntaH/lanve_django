from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('v1/favorite/', views.CreateFavoriteView.as_view(), name='create_favorite'),
]
