# Generated by Django 3.1.4 on 2021-03-28 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0012_token_recipe_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipetokenfrequency',
            name='recipe_length',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
