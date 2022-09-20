from django.contrib import admin

from apps.recipes.models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'name',
                    'measurement_unit',
                ),
            },
        ),
        (
            'Техническая информация',
            {
                'classes': (
                    'collapse',
                ),
                'fields': (
                    'id',
                ),
            },
        ),
    )

    readonly_fields = (
        'id',
    )
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
    )
