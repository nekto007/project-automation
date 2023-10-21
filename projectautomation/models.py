from django.db import models


class Levels(models.Model):
    title = models.TextField(
        'Название Группы',
        max_length=200,
        blank=True,
    )


class TimeSlot(models.Model):
    start_time = models.CharField(
        verbose_name='Слот времени',
        max_length=200)

    def __str__(self):
        return f'{self.start_time}'

    class Meta:
        verbose_name = 'Временной слот'
        verbose_name_plural = 'Временные слоты'


class PM(models.Model):
    name = models.CharField(
        verbose_name='Имя ПМ',
        max_length=200)
    email = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='email')
    time_slots = models.ManyToManyField(
        TimeSlot,
        verbose_name='Временной слот',
        max_length=200,
        related_name='pms'
    )

    def __str__(self):
        return f'ПМ {self.name}'

    def get_time_slots(self):
        return " | ".join([str(time_slot) for time_slot in self.time_slots.all()])

    class Meta:
        verbose_name = 'ПМа'
        verbose_name_plural = 'ПМы'


class Student(models.Model):
    first_name = models.CharField(verbose_name='Имя',
                                  max_length=200)
    last_name = models.CharField(verbose_name='Фамилия',
                                 null=True,
                                 blank=True,
                                 max_length=200)
    email = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='email')
    level = models.ForeignKey(
        Levels,
        verbose_name='Уровень',
        related_name='student',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    def __str__(self):
        return f'Ученик {self.first_name} {self.last_name}'


    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'


class Group(models.Model):
    title = models.TextField(
        'Название Группы',
        max_length=200,
        blank=True,
    )
    description = models.TextField(
        'Описание',
        max_length=200,
        blank=True,
    )
    time_slot = models.ForeignKey(
        TimeSlot,
        verbose_name='Время группы',
        related_name='groups',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    pm = models.ForeignKey(
        PM,
        verbose_name='ПМ группы',
        related_name='groups',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    trello_id = models.IntegerField(unique=True)
    students = models.ManyToManyField(
        Student,
        verbose_name='Студенты',
        related_name='students',
        blank=True
    )
    is_complete = models.BooleanField(
        'заполнена ли группа',
        default=False,
        db_index=True,
    )

    def __str__(self):
        return f'{self.pm.name}-{self.time_slot.timeslot}'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Project(models.Model):
    title = models.CharField(verbose_name='Наименование рассылки',
                             max_length=200)
    description = models.CharField(verbose_name='Описание',
                             max_length=200)
    start_at = models.DateTimeField('Начало проекта',
                                    null=True,
                                    blank=True)
    level = models.ForeignKey(
        Levels,
        verbose_name='Уровень',
        related_name='project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Дата рассылки'
        verbose_name_plural = 'Даты рассылок'
