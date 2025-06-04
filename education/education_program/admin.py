from django.contrib import admin
from .models import Student, EducationProgram, Enrollment, Discipline


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    fields = ("program", "start_year", "gpa", "created_at")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "date_of_birth", "programs_count")
    list_filter = ("date_of_birth",)
    search_fields = ("full_name", "email")
    inlines = (EnrollmentInline,)

    @admin.display(description="Кол-во ОП")
    def programs_count(self, obj):
        return obj.enrollment_set.count()


@admin.register(EducationProgram)
class ProgramAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "head_name",
        "manager_name",
        "students_count",
    )
    search_fields = ("title", "head_name", "manager_name")
    inlines = (EnrollmentInline,)

    @admin.display(description="Студентов")
    def students_count(self, obj):
        return obj.enrollment_set.count()


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ("name", "program", "credits")
    list_filter = ("program",)
    search_fields = ("name", "program__title")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "student", "program", "start_year",
        "group", "study_form", "status",
        "gpa", "created_at",
    )
    list_filter = ("start_year", "program", "study_form", "status")
    search_fields = (
        "student__full_name",
        "student__email",
        "program__title",
        "group",
    )
    autocomplete_fields = ("student", "program")
    date_hierarchy = "created_at"
    ordering = ("-id",)
