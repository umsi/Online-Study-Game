from django.contrib import admin

from .models import InvestmentGameUser, Investment


class InvestmentGameUserAdmin(admin.ModelAdmin):
    pass


class InvestmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(InvestmentGameUser, InvestmentGameUserAdmin)
admin.site.register(Investment, InvestmentAdmin)
