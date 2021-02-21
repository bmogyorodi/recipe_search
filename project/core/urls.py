from django.urls import path, re_path
from . import views

app_name = "core"
urlpatterns = [
    path('', views.home, name="home")
]
