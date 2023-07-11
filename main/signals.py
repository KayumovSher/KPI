from .models import *
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver



from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=SportModel)
@receiver(post_save, sender=BookModel)
@receiver(post_save, sender=WorkModel)
@receiver(post_save, sender=EvrikaModel)

def update_kpi_overall(sender, instance, created, **kwargs):
    if created is None:
        # kpi = instance.kpi
        # kpi.calculate_general()
        # kpi.save()
        pass
    else:
        kpi = instance.kpi
        kpi.calculate_general()
        kpi.save()



