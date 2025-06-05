import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Min, Max, Count
from .forms import StudentForm, ProgramForm, EnrollmentForm, DisciplineForm
from .models import Student, EducationProgram, Enrollment, Discipline


def index(request):
    return render(request, "education_program/index.html")


def student_create(request):
    form = StudentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("education_program:index")
    return render(request, "education_program/student_form.html", {"form": form})


def program_create(request):
    form = ProgramForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("education_program:index")
    return render(request, "education_program/program_form.html", {"form": form})


def discipline_create(request):
    form = DisciplineForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("education_program:discipline_list")
    return render(request, "education_program/discipline_form.html", {"form": form})


def enrollment_create(request):
    form = EnrollmentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("education_program:table")
    return render(request, "education_program/enrollment_form.html", {"form": form})


def discipline_list(request):
    disciplines = Discipline.objects.select_related("program").all().order_by("name")
    return render(request, "education_program/discipline_list.html", {
        "disciplines": disciplines,
    })


def table(request):
    """
    Вывод всех Enrollment с расширенной фильтрацией/сортировкой через GET-параметры:

      Фильтры (GET):
        ?year=<год> – зачисления только указанного года
        &program=<id_program> – зачисления по определённой программе
        &study_form=<значение> – фильтр по форме обучения
        &status=<значение> – фильтр по статусу
        &group=<строка> – фильтр по вхождению в поле «группа»

      Сортировка (GET):
        ?sort=<поле> – сортировка по возрастанию (если без «-»)
        ?sort=-<поле> – сортировка по убыванию (если с «-»)
        Допустимые поля для sort:
          id, -id,
          gpa, -gpa,
          start_year, -start_year,
          student__full_name, -student__full_name,
          program__title, -program__title,
          group, -group
    """
    qs = Enrollment.objects.select_related("student", "program")

    year = request.GET.get("year")
    program_id = request.GET.get("program")
    study_form = request.GET.get("study_form")
    status = request.GET.get("status")
    group_q = request.GET.get("group")

    if year:
        qs = qs.filter(start_year=year)

    if program_id:
        qs = qs.filter(program_id=program_id)

    if study_form:
        qs = qs.filter(study_form=study_form)

    if status:
        qs = qs.filter(status=status)

    if group_q:
        qs = qs.filter(group__icontains=group_q)

    SORTABLE_FIELDS = [
        "student__full_name",
        "student__date_of_birth",
        "program__title",
        "group",
        "start_year",
        "gpa",
    ]

    current_sort = request.GET.get("sort", "-id")
    allowed_sort = set(f for f in SORTABLE_FIELDS) | set(f"-{f}" for f in SORTABLE_FIELDS) | {"id", "-id"}
    if current_sort not in allowed_sort:
        current_sort = "-id"

    qs = qs.order_by(current_sort)

    stats = qs.aggregate(
        count=Count("gpa"),
        avg=Avg("gpa"),
        min=Min("gpa"),
        max=Max("gpa"),
    )

    get_params = request.GET.copy()
    sort_urls = {}
    for field in SORTABLE_FIELDS:
        if current_sort == field:
            next_sort = f"-{field}"
        elif current_sort == f"-{field}":
            next_sort = field
        else:
            next_sort = field

        params = get_params.copy()
        params["sort"] = next_sort
        sort_urls[field] = params.urlencode()

    programs = EducationProgram.objects.all().order_by("title")
    study_forms = Enrollment.FORM_CHOICES
    statuses = Enrollment.STATUS_CHOICES

    context = {
        "enrollments": qs,
        "stats": stats,
        "current_year": year or "",
        "current_program": int(program_id) if program_id else "",
        "current_study_form": study_form or "",
        "current_status": status or "",
        "current_group": group_q or "",
        "current_sort": current_sort,
        "programs": programs,
        "study_forms": study_forms,
        "statuses": statuses,
        "sort_urls": sort_urls,
    }
    return render(request, "education_program/table.html", context)
