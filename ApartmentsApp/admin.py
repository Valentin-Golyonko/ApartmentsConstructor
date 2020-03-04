from django.contrib import admin

from ApartmentsApp.models import Apartments, Address, Room


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


class AddressInline(admin.StackedInline):
    model = Address
    extra = 0


class RoomInline(admin.StackedInline):
    model = Room
    extra = 0


@admin.register(Apartments)
class ApartmentsAdmin(admin.ModelAdmin):
    inlines = (AddressInline, RoomInline,)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass
