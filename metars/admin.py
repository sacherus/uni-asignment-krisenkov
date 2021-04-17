from django.contrib import admin
from .models import Metar, SkyCondition


class SkyConditionAdmin(admin.TabularInline):
    model = SkyCondition
    extra = 0


class MetarAdmin(admin.ModelAdmin):
    list_display = ("station_id", "observation_time")
    inlines = [
        SkyConditionAdmin,
    ]


admin.site.register(Metar, MetarAdmin)
