from django.contrib import admin

from .models import GamesUser


class GamesUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(GamesUser, GamesUserAdmin)
