from django.contrib import admin
from django.urls import path, include
from .api import *

urlpatterns = [
    path('signup/', signup),
    path('login/', login_by_username_phone_email),
    path('profile/', ProfileApi.as_view()),

]