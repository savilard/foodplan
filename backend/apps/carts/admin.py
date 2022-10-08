from django.contrib import admin

from apps.carts.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    show_full_result_count = False
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'owner',
                    'recipes',
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
        'owner',
    )
    raw_id_fields = (
        'owner',
    )
    search_fields = (
        'owner__username',
        'owner__email',
    )
