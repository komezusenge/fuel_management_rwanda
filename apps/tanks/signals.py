from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tank, TankStatus


@receiver(post_save, sender=Tank)
def check_tank_level(sender, instance, **kwargs):
    """Update tank status when level changes."""
    pct = instance.fill_percentage
    if pct <= 0:
        new_status = TankStatus.EMPTY
    elif pct <= 10:
        new_status = TankStatus.CRITICAL
    elif pct <= 20:
        new_status = TankStatus.LOW
    else:
        new_status = TankStatus.NORMAL

    if instance.status != new_status:
        Tank.objects.filter(pk=instance.pk).update(status=new_status)
