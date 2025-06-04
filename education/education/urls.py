from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", RedirectView.as_view(url="/education/", permanent=False)),
    path("education/", include("education_program.urls", namespace="education_program")),
]
