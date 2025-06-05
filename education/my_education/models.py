from django.db import models
from django.urls import reverse


class Profile(models.Model):
    full_name = models.CharField("ФИО", max_length=200)
    #photo = models.ImageField("Фото", upload_to="my_education/profiles/", blank=True)
    email = models.EmailField("E-mail")
    phone = models.CharField("Телефон", max_length=20, blank=True)
    resume = models.TextField("Резюме", blank=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.full_name


class Program(models.Model):
    title = models.CharField("Название ОП", max_length=300)
    link = models.URLField("Ссылка на сайт ОП", blank=True)
    description = models.TextField("Что я буду изучать", blank=True)
    skills = models.TextField("Чему научусь", blank=True)
    advantages = models.TextField("Преимущества программы", blank=True)
    prospects = models.TextField("Перспективы после обучения", blank=True)

    class Meta:
        verbose_name = "Образовательная программа"
        verbose_name_plural = "Образовательные программы"

    def __str__(self):
        return self.title


class ProgramStaff(models.Model):
    ROLE_HEAD = "head"
    ROLE_MANAGER = "manager"
    ROLE_CHOICES = [
        (ROLE_HEAD, "Академический руководитель"),
        (ROLE_MANAGER, "Менеджер программы"),
    ]

    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        verbose_name="Программа",
        related_name="staff"
    )
    full_name = models.CharField("ФИО", max_length=200)
    #photo = models.ImageField("Фото", upload_to="my_education/staff/", blank=True)
    email = models.EmailField("E-mail")
    phone = models.CharField("Телефон", max_length=20, blank=True)
    role = models.CharField("Роль", max_length=20, choices=ROLE_CHOICES, default=ROLE_MANAGER)

    class Meta:
        verbose_name = "Сотрудник ОП"
        verbose_name_plural = "Сотрудники ОП"
        ordering = ["role", "full_name"]  # head → first, then managers

    def __str__(self):
        return f"{self.get_role_display()}: {self.full_name}"


class Classmate(models.Model):
    program = models.ForeignKey(
        Program,
        on_delete=models.SET_NULL,
        verbose_name="Программа",
        related_name="classmates",
        null=True,
        blank=True
    )
    full_name = models.CharField("ФИО", max_length=200)
    #photo = models.ImageField("Фото", upload_to="my_education/classmates/", blank=True)
    email = models.EmailField("E-mail")
    phone = models.CharField("Телефон", max_length=20, blank=True)

    class Meta:
        verbose_name = "Сокурсник"
        verbose_name_plural = "Сокурсники"
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class GenericPage(models.Model):
    page_slug = models.SlugField(
        "Уникальный слаг",
        max_length=100,
        unique=True,
        help_text="URL: /my-education/page/<page_slug>/"
    )
    page_title = models.CharField("Заголовок страницы", max_length=200)
    menu_label = models.CharField(
        "Название в навигации",
        max_length=100,
        blank=True,
        help_text="Если пусто или menu_order=0 → не показывать в меню"
    )
    menu_order = models.IntegerField(
        "Позиция в навигации",
        default=0,
        help_text=">0 → показывать; чем выше число, тем раньше в меню"
    )
    content_html = models.TextField(
        "HTML-контент страницы",
        default="<p>Здесь ваш HTML-контент</p>"
    )
    updated_at = models.DateTimeField("Последнее изменение", auto_now=True)

    class Meta:
        verbose_name = "Универсальная страница"
        verbose_name_plural = "Универсальные страницы"
        ordering = ["-menu_order", "page_title"]

    def __str__(self):
        return f"{self.page_title} ({self.page_slug})"

    def get_absolute_url(self):
        return reverse("my_education:generic_page", kwargs={"page_slug": self.page_slug})
