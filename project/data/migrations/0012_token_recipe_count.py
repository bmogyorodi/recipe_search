# Generated by Django 3.1.4 on 2021-03-25 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0011_auto_20210324_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='recipe_count',
            field=models.PositiveIntegerField(null=True),
        ),
    ]