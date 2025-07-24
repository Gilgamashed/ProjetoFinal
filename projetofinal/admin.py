from django.contrib import admin

from projetofinal.models import Convite


@admin.register(Convite)
class ConviteAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'created_by', 'expires', 'accepted')
    list_filter = ('role', 'accepted')
    search_fields = ('email', 'created_by__email')

# Register your models here.
