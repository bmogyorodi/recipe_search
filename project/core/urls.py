from django.urls import path, re_path
from . import views

app_name = "core"
urlpatterns = [
    path('', views.home, name="home"),
    path('new', views.new, name="new")
    # re_path(
    #         r'^ingredient-autocomplete/$',
    #         views.IngredientAutoComplete.as_view(),
    #         name='ingredient-autocomplete',
    #     )
]
