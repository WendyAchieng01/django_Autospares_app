from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction, Order

@receiver(post_save, sender=Transaction)
def update_order_paid_status(sender, instance, **kwargs):
    if instance.status == 'Success':
        order = instance.order
        order.is_paid = True
        order.save(update_fields=['is_paid'])