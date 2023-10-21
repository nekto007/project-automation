from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student


# triggred when User object is created
@receiver(post_save, sender=Student)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print(f'Send email to: {instance.email}')
