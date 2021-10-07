from django.contrib import admin

from .models import AdditionalUserInformation


@admin.register(AdditionalUserInformation)
class AdditionalUserInformationAdmin(admin.ModelAdmin):
    list_display = ['user', 'inn', 'account']
    search_fields = ['inn', 'user__username']
