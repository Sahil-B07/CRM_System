from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

from .views import VendorViewSet
from .models import PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
def purchase_order_saved(sender, instance, **kwargs):
    VendorViewSet.performance(self=VendorViewSet,request=None, pk=instance.vendor.id)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
