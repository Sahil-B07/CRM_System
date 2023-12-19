from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from .views import VendorViewSet

from .models import PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
def purchase_order_saved(sender, instance, **kwargs):
    VendorViewSet.performance(self=VendorViewSet,request=None, pk=instance.vendor.id)
