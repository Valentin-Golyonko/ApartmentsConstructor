from django.contrib import admin

from ApartmentsApp.models import (Apartments, Room, Chair)


class ChairInline(admin.StackedInline):
    model = Chair
    extra = 0


class RoomInline(admin.StackedInline):
    model = Room
    extra = 0


@admin.register(Apartments)
class ApartmentsAdmin(admin.ModelAdmin):
    inlines = (RoomInline,)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = (ChairInline,)


@admin.register(Chair)
class ChairAdmin(admin.ModelAdmin):
    pass
