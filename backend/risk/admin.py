from django.contrib import admin
from risk.models import Risk, Company, RiskItem, PredefinedSearch


class RiskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type')
    list_filter = ('type',)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')

class PredefinedSearchAdmin(admin.ModelAdmin):
    list_display = ('name', 'search_string', 'is_global', 'description')

class RiskItemAdmin(admin.ModelAdmin):
    list_display = ('project', 'from_company', 'to_company', 'risk', 'subrisk')

admin.site.register(Risk, RiskAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(PredefinedSearch, PredefinedSearchAdmin)
admin.site.register(RiskItem, RiskItemAdmin)
