from django.contrib import admin

from user.models import City, Profile, State, User


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "state")
    list_filter = ("state",)
    ordering = ("name",)
    search_fields = ("name",)


admin.site.register(User)
admin.site.register(State)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "name", "celular", "birthday", "city",)
    # list_filter = ("user",)
    ordering = ("user",)
    search_fields = ("name",)
