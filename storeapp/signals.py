
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import CustomUser

@receiver(m2m_changed, sender=CustomUser.groups.through)
def set_staff_status(sender, instance, action, **kwargs):
    if action == 'post_add':
        if Group.objects.get(name='Moderators') in instance.groups.all():
            instance.is_staff = True
            instance.save()