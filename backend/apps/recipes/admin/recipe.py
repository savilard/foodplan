from django.contrib import admin
from django.utils.html import format_html

from apps.recipes.models import Recipe


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    classes = ('collapse',)
    raw_id_fields = (
        'ingredient',
    )
    fields = (
        'ingredient',
        'amount',
    )
    extra = 1


class RecipeTagInline(admin.TabularInline):
    model = Recipe.tags.through
    classes = ('collapse',)
    raw_id_fields = (
        'tag',
    )
    exclude = (
        'modified',
    )
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    show_full_result_count = False
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'author',
                    'name',
                    'text',
                    'image',
                    'get_image_preview',
                    'cooking_time',
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

    inlines = (
        RecipeIngredientInline,
        RecipeTagInline,
    )
    readonly_fields = (
        'id',
        'get_image_preview',
    )
    list_display = (
        'name',
        'author',
        'cooking_time',
    )
    search_fields = (
        'name',
    )
    raw_id_fields = (
        'author',
    )

    @admin.display(description='превью')
    def get_image_preview(self, obj):
        if not obj.image:
            return 'выберите картинку'
        return format_html('<img src="{url}" style="max-height: 200px;"/>', url=obj.image.url)
