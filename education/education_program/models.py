from django.db import models
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r"^\+?\d{7,15}$",
    message="Телефон должен быть в формате +79998887766 (7-15 цифр).",
)


class Student(models.Model):
    full_name = models.CharField("ФИО", max_length=200)
    email = models.EmailField("E-mail", unique=True)
    phone = models.CharField(
        "Телефон", max_length=20, blank=True, validators=[phone_validator]
    )
    date_of_birth = models.DateField("Дата рождения", null=True, blank=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = "студент"
        verbose_name_plural = "студенты"

    def __str__(self):
        return self.full_name


class EducationProgram(models.Model):
    title = models.CharField("Название ОП", max_length=300, unique=True)
    description = models.TextField("Описание ОП", blank=True)
    head_name = models.CharField("Академический руководитель — ФИО", max_length=200, blank=True)
    head_email = models.EmailField("E-mail академ. руководителя", blank=True)
    manager_name = models.CharField("Менеджер программы — ФИО", max_length=200, blank=True)
    manager_email = models.EmailField("E-mail менеджера", blank=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "образовательная программа"
        verbose_name_plural = "образовательные программы"

    def __str__(self):
        return self.title


class Discipline(models.Model):
    program = models.ForeignKey(
        EducationProgram,
        on_delete=models.CASCADE,
        verbose_name="Образовательная программа",
        related_name="disciplines"
    )
    name = models.CharField("Название дисциплины", max_length=200)
    description = models.TextField("Краткое описание", blank=True)
    credits = models.PositiveSmallIntegerField("Кредиты", default=0)

    class Meta:
        ordering = ["name"]
        verbose_name = "дисциплина"
        verbose_name_plural = "дисциплины"

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="Студент",
    )
    program = models.ForeignKey(
        EducationProgram,
        on_delete=models.CASCADE,
        verbose_name="Программа",
    )

    group = models.CharField("Учебная группа", max_length=20, blank=True)
    FORM_CHOICES = [
        ("full_time", "Очная"),
        ("part_time", "Очно-заочная"),
    ]
    study_form = models.CharField("Форма обучения", max_length=15, choices=FORM_CHOICES, default="full_time")
    STATUS_CHOICES = [
        ("active", "Учится"),
        ("academic_leave", "Академический отпуск"),
        ("expelled", "Отчислен"),
    ]
    status = models.CharField("Статус", max_length=15, choices=STATUS_CHOICES, default="active")

    start_year = models.PositiveSmallIntegerField("Год поступления")
    gpa = models.DecimalField("Средний балл (GPA)", max_digits=4, decimal_places=2)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "зачисление"
        verbose_name_plural = "зачисления"
        constraints = [
            models.UniqueConstraint(
                fields=("student", "program", "start_year"),
                name="unique_enrollment_per_year",
            )
        ]

    def __str__(self):
        return f"{self.student} — {self.program} ({self.start_year})"
