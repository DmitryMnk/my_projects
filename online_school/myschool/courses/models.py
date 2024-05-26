from django.db import models


class CourseCategory(models.Model):
    name = models.CharField(max_length=30, verbose_name='Категория курса', unique=True)
    preview = models.ImageField(verbose_name='Превью', upload_to='courses/cat_preview')

    def __str__(self):
        return f'{self.name}'


class CourseLevel(models.Model):
    name = models.CharField(max_length=30, verbose_name='Уровень курса', unique=True)

    def __str__(self):
        return f'{self.name}'


class CourseSubCategory(models.Model):
    name = models.CharField(max_length=30, verbose_name='Подкатегория', unique=True)

    def __str__(self):
        return f'{self.name}'


class Course(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, verbose_name='Категория')
    subcategory = models.ForeignKey(CourseSubCategory, on_delete=models.CASCADE, verbose_name='Подкатегория')
    level = models.ForeignKey(CourseLevel, on_delete=models.CASCADE, verbose_name='Уровень')
    preview = models.ImageField(verbose_name='Превью', upload_to='courses/preview')
    price = models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Стоимость')

    def __str__(self):
        return f'{self.name}-{self.category.name}-{self.level}-{self.price}'
