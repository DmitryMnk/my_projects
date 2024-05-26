# Generated by Django 5.0.5 on 2024-05-20 06:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_coursesubcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursesubcategory',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='Подкатегория'),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название')),
                ('preview', models.ImageField(upload_to='courses/preview', verbose_name='Превью')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Стоимость')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.coursecategory', verbose_name='Категория')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.courselevel', verbose_name='Уровень')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.coursesubcategory', verbose_name='Подкатегория')),
            ],
        ),
    ]
