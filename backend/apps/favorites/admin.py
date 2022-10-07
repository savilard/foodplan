from django.contrib import admin

from apps.favorites.models import Favorites


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    show_full_result_count = False
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'user',
                    'recipe',
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
        'user',
        'recipe',
    )
    raw_id_fields = (
        'user',
        'recipe',
    )
    search_fields = (
        'user__username',
        'user__email',
    )
