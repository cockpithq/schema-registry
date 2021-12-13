from django.contrib import admin

from schema_registry.models import Schema, Version


class VersionAdminInline(admin.StackedInline):
    extra = 0
    model = Version
    readonly_fields = ('number',)


@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    inlines = (VersionAdminInline,)
