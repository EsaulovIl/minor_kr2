from django.urls import path
from . import views

app_name = "education_program"

urlpatterns = [
    path("", views.index, name="index"),
    path("student/add/", views.student_create, name="student_add"),
    path("program/add/", views.program_create, name="program_add"),
    path("enroll/add/", views.enrollment_create, name="enroll_add"),
    path("discipline/add/", views.discipline_create, name="discipline_add"),
    path("disciplines/", views.discipline_list, name="discipline_list"),
    path("table/", views.table, name="table"),
]
