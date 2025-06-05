from django.urls import path
from . import views

app_name = "my_education"

urlpatterns = [
    path("", views.home, name="home"),
    path("me/", views.profile_detail, name="profile"),
    path("program/", views.program_detail, name="program"),
    path("program/staff/", views.program_staff, name="program_staff"),
    path("mates/", views.classmate_list, name="mates"),
    path("page/<slug:page_slug>/", views.generic_page, name="generic_page"),
]
