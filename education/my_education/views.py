from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Profile, Program, ProgramStaff, Classmate, GenericPage


def _get_generic_nav_items():
    """
    Вспомогательная функция: возвращает queryset тех GenericPage,
    где menu_order > 0, отсортированных по -menu_order.
    Будем использовать её везде, чтобы передавать в шаблон.
    """
    return GenericPage.objects.filter(menu_order__gt=0).order_by("-menu_order")


def home(request):
    """
    Простая страница-обзвонка: можно редиректить на /my-education/me/ или
    отображать набор ссылок.
    """
    return render(request, "my_education/home.html")


def profile_detail(request):
    """
    Страница «Я». Берём единственный объект Profile или 404.
    """
    profile = get_object_or_404(Profile)
    return render(request, "my_education/profile_detail.html", {"profile": profile})


def program_detail(request):
    """
    Страница «Описание образовательной программы». Берём первый Program.
    """
    program = Program.objects.first()
    if not program:
        return render(request, "my_education/no_program.html")
    return render(request, "my_education/program_detail.html", {"program": program})


def program_staff(request):
    """
    Страница «Менеджмент ОП»: список сотрудников (руководитель + менеджеры).
    """
    program = Program.objects.first()
    if not program:
        return render(request, "my_education/no_program.html")

    staff = ProgramStaff.objects.filter(program=program).order_by("role", "full_name")
    return render(request, "my_education/program_staff.html", {
        "program": program,
        "staff": staff,
    })


def classmate_list(request):
    """
    Страница «Мои сокурсники»:
      - фильтрация по GET-параметру ?q=
      - сортировка по ?sort=<поле> или ?sort=-<поле> (разрешенные: full_name, email, phone)
    """
    program = Program.objects.first()
    if not program:
        return render(request, "my_education/no_program.html")

    qs = Classmate.objects.filter(program=program)

    # Поисковая строка
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            Q(full_name__icontains=q) |
            Q(email__icontains=q) |
            Q(phone__icontains=q)
        )

    # Сортировка
    sort = request.GET.get("sort", "full_name")
    allowed_sort = {"full_name", "-full_name", "email", "-email", "phone", "-phone"}
    if sort not in allowed_sort:
        sort = "full_name"
    qs = qs.order_by(sort)

    return render(request, "my_education/classmate_list.html", {
        "classmates": qs,
        "current_q": q,
        "current_sort": sort,
        "program": program,
    })


def generic_page(request, page_slug):
    """
    Вьюха для «универсальных» страниц. Берёт GenericPage по page_slug,
    строит меню из всех GenericPage(menu_order>0) и рендерит контент.
    """
    page = get_object_or_404(GenericPage, page_slug=page_slug)
    generic_nav_items = GenericPage.objects.filter(menu_order__gt=0).order_by("-menu_order")

    return render(request, "my_education/generic_page.html", {
        "page": page,
        "generic_nav_items": generic_nav_items,
    })
