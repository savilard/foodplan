# Generated by Django 3.2.14 on 2022-09-20 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_add_ingredient_model'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ingredient', 'verbose_name_plural': 'Ingredients'},
        ),
    ]
