import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.urls import reverse

from .models import Group, Project, Student


# triggred when User object is created
@receiver(post_save, sender=Project)
def create_profile(sender, instance, created, **kwargs):
    if created:
        students = instance.level.student.all()
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login(
            settings.SENDER_EMAIL_LOGIN,
            settings.SENDER_EMAIL_PASSWORD)

        for student in students:
            msg = MIMEMultipart()

            page_student = reverse("choose_time",
                                   args=[instance.id, student.id])

            message = f'Уважаемый {student.first_name}\n' \
                      f'Приглашаем на коммандный проект {instance.title}\n' \
                      f'Выберете время: ' \
                      f'http://{settings.ALLOWED_HOSTS[0]}{page_student}'

            msg['From'] = settings.SENDER_EMAIL_LOGIN
            msg['To'] = student.email
            msg['Subject'] = \
                f'Приглашение в командный проект "{instance.title}"'

            msg.attach(MIMEText(message, 'plain'))

            smtpObj.send_message(msg)


@receiver(post_save, sender=Group)
def create_group(sender, instance, created, **kwargs):
    if (not created) and \
            (not instance.trello_url) and \
            (not instance.telegram_chat_id) and \
            (instance.is_complete):
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login(
            settings.SENDER_EMAIL_LOGIN,
            settings.SENDER_EMAIL_PASSWORD)
        message = f'Привет {instance.pm.name}\n' \
                  f'Группа "{instance.title}" собрана\n' \
                  f'Выбранное время: {instance.time_slot}.\n' \
                  f'Добавьте данные телеграм и трело в базу.'

        msg = MIMEMultipart()
        msg['From'] = settings.SENDER_EMAIL_LOGIN
        msg['To'] = instance.pm.email
        msg['Subject'] = \
            f'Собрана команда "{instance.time_slot}" ' \
            f'проекта "{instance.title}"'

        msg.attach(MIMEText(message, 'plain'))

        smtpObj.send_message(msg)
    elif (not created) and \
            (instance.trello_url) and \
            (instance.telegram_chat_id) and \
            (instance.is_complete):
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login(
            settings.SENDER_EMAIL_LOGIN,
            settings.SENDER_EMAIL_PASSWORD)
        for student in instance.students.all():
            msg = MIMEMultipart()

            message = \
                f'Уважаемый {student.first_name}\n' \
                f'Вы записаны на коммандный проект {instance.project.title}\n' \
                f'Выбранное время созвона: {instance.time_slot}\n\n' \
                f'Ссылка на телеграм бота: {instance.telegram_chat_id}\n' \
                f'Ссылка на трело: {instance.trello_url}'

            msg['From'] = settings.SENDER_EMAIL_LOGIN
            msg['To'] = student.email
            msg['Subject'] = \
                f'Командный проект "{instance.title}"'

            msg.attach(MIMEText(message, 'plain'))

            smtpObj.send_message(msg)


@receiver(m2m_changed, sender=Group.students.through)
def update_is_complete(sender, instance, **kwargs):
    project_groups = Group.objects.filter(project=instance.project)
    for group in project_groups:
        student_count = group.students.count()
        if student_count == 3 or not Student.objects.filter(level=group.project.level).exclude(
                students__project=group.project).exists():
            group.is_complete = True
        else:
            group.is_complete = False
        group.save()
