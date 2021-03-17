from django.urls import path
from . import views


app_name = "core"
urlpatterns = [
    path('search', views.search, name="search"),
    path('', views.home, name="home")
]
