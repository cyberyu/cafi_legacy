from django.contrib import admin
from google.models import Search, SearchResult, GeoSearch


class GeoSearchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'lat', 'lng')


admin.site.register(Search)
admin.site.register(SearchResult)
admin.site.register(GeoSearch, GeoSearchAdmin)