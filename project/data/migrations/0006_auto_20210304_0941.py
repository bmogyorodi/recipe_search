# Generated by Django 3.1.4 on 2021-03-04 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_recipetoken_index'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeingredient',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='recipeingredient',
            name='unit',
        ),
    ]
