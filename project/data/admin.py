from django.contrib import admin
from django.db.models import Count

from .models import (Recipe, RecipeIngredient, RecipeToken,
                     Ingredient, Token, Tag, Source)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "source", "ratings", "total_time", "yields")


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("title", "get_num_recipes")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(num_recipes=Count("recipe"))
        return qs

    def get_num_recipes(self, obj):
        return obj.num_recipes
    get_num_recipes.admin_order_field = 'num_recipes'
    get_num_recipes.short_description = '# of recipes'


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ("title", "get_num_recipe_tokens")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(num_recipe_tokens=Count("recipes"))
        return qs

    def get_num_recipe_tokens(self, obj):
        return obj.num_recipe_tokens
    get_num_recipe_tokens.admin_order_field = 'num_recipe_tokens'
    get_num_recipe_tokens.short_description = '# of recipe tokens'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title", "get_num_recipes")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(num_recipes=Count("recipe"))
        return qs

    def get_num_recipes(self, obj):
        return obj.num_recipes
    get_num_recipes.admin_order_field = 'num_recipes'
    get_num_recipes.short_description = '# of recipes'


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("source_id", "title", "url", "favicon")
