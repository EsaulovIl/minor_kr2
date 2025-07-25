# Generated by Django 5.2.2 on 2025-06-04 20:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_program', '0003_enrollment_group_enrollment_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название дисциплины')),
                ('description', models.TextField(blank=True, verbose_name='Краткое описание')),
                ('credits', models.PositiveSmallIntegerField(default=0, verbose_name='Кредиты')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disciplines', to='education_program.educationprogram', verbose_name='Образовательная программа')),
            ],
            options={
                'verbose_name': 'дисциплина',
                'verbose_name_plural': 'дисциплины',
                'ordering': ['name'],
            },
        ),
    ]
