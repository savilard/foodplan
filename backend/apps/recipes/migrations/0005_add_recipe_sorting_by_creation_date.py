# Generated by Django 3.2.14 on 2022-10-04 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_add_recipe_sorting_by_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-created',), 'verbose_name': 'Recipe', 'verbose_name_plural': 'Recipes'},
        ),
    ]
