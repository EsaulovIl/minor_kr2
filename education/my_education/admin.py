from django.contrib import admin
from .models import Profile, Program, ProgramStaff, Classmate, GenericPage


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone")
    search_fields = ("full_name", "email", "phone")


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


# inlines = (ProgramStaffInline, ClassmateInline)


@admin.register(ProgramStaff)
class ProgramStaffAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role", "program", "email", "phone")
    list_filter = ("role", "program")
    search_fields = ("full_name", "email", "program__title")
    raw_id_fields = ("program",)


@admin.register(Classmate)
class ClassmateAdmin(admin.ModelAdmin):
    list_display = ("full_name", "program", "email", "phone")
    list_filter = ("program",)
    search_fields = ("full_name", "email", "program__title")
    raw_id_fields = ("program",)


@admin.register(GenericPage)
class GenericPageAdmin(admin.ModelAdmin):
    list_display = ("page_title", "page_slug", "menu_label", "menu_order", "updated_at")
    list_filter = ("menu_order",)
    search_fields = ("page_title", "page_slug", "menu_label")
    ordering = ("-menu_order", "page_title")
    prepopulated_fields = {"page_slug": ("page_title",)}
