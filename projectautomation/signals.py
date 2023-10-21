import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Project


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

            message = f'Уважаемый {student.first_name}\n'\
                      f'Приглашаем на коммандный проект {instance.title}\n'\
                      f'Выберете время: '\
                      f'http://127.0.0.1:8000/'\
                      f'to_project/{instance.id}&{student.id}'

            msg['From'] = settings.SENDER_EMAIL_LOGIN
            msg['To'] = student.email
            msg['Subject'] = f'Приглашение в командный проект "{instance.title}"'

            msg.attach(MIMEText(message, 'plain'))

            smtpObj.send_message(msg)
