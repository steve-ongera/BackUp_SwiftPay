from django.urls import path

from . import views

app_name = "pos"
urlpatterns = [
    path('', views.index, name='index'),
    path('help-and-support/', views.help_and_support, name='help_and_support'),
]
