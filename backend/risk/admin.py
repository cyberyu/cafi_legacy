from django.contrib import admin
from risk.models import Risk, Company


class RiskAdmin(admin.ModelAdmin):
    list_display = ('name', 'search_string', 'description')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')

admin.site.register(Risk, RiskAdmin)
admin.site.register(Company, CompanyAdmin)
