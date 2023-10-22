import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from .models import Group, Project


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

            message = f'Уважаемый {student.first_name}\n'\
                      f'Приглашаем на коммандный проект {instance.title}\n'\
                      f'Выберете время: '\
                      f'http://{settings.ALLOWED_HOSTS[0]}{page_student}'

            msg['From'] = settings.SENDER_EMAIL_LOGIN
            msg['To'] = student.email
            msg['Subject'] =\
                f'Приглашение в командный проект "{instance.title}"'

            msg.attach(MIMEText(message, 'plain'))

            smtpObj.send_message(msg)


@receiver(post_save, sender=Group)
def create_group(sender, instance, created, **kwargs):
    if (not created) and\
       (not instance.trello_url) and\
       (not instance.telegram_chat_id) and\
       (instance.is_complete):
        print(f'-=-=-=-=-=-=-=-=-Send {instance.pm.name} to email PM: {instance.pm.email}')
    elif (not created) and\
         (instance.trello_url) and\
         (instance.telegram_chat_id) and\
         (instance.is_complete):
        print(f'-=-=-=-=-=-=-=-=-Send students email: {instance.students}')
