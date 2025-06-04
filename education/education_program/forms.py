from django import forms
from .models import Student, EducationProgram, Enrollment, Discipline


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ("full_name", "email", "phone", "date_of_birth")
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }


class ProgramForm(forms.ModelForm):
    class Meta:
        model = EducationProgram
        fields = (
            "title",
            "description",
            "head_name",
            "head_email",
            "manager_name",
            "manager_email",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class DisciplineForm(forms.ModelForm):
    class Meta:
        model = Discipline
        fields = ("program", "name", "description", "credits")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ("student", "program", "start_year", "group", "study_form", "status", "gpa",)
        widgets = {
            "gpa": forms.NumberInput(attrs={"step": "0.01"}),
        }
