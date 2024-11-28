from django.urls import path
from .views import login_view, register_user , custom_logout
from django.contrib.auth.views import LogoutView

app_name = "authentication"
urlpatterns = [
    path('accounts/login/', login_view, name="login"),
    path('accounts/register/', register_user, name="register"),
    path("logout",  custom_logout , name="logout")
]
