import csv

from django.contrib import admin
from django.db import models
from django.http import HttpResponse
from django.forms import Textarea

from .models import InvestmentGameUser, Investment


class InvestmentGameUserAdmin(admin.ModelAdmin):
    pass


class InvestmentAdmin(admin.ModelAdmin):
    actions = ["download_csv"]
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 1, "cols": 40})}
    }

    def download_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow(getattr(obj, field) for field in field_names)

        return response

    download_csv.short_description = "Download CSV for selected Investment instances"


admin.site.register(InvestmentGameUser, InvestmentGameUserAdmin)
admin.site.register(Investment, InvestmentAdmin)
