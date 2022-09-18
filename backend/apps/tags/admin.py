from django.contrib import admin

from apps.tags.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'name',
                    'color',
                    'slug',
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
                    'uuid',
                ),
            },
        ),
    )

    readonly_fields = (
        'uuid',
    )
    list_display = (
        'name',
        'slug',
    )
    search_fields = (
        'name',
    )
