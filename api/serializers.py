from rest_framework import serializers
from .models import *

class VendorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vendor
        fields= '__all__'

class MetricSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Metrics
        fields= '__all__'
        read_only=True

class POSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields= '__all__'
        # exclude = ['date_updated',]

class PurchaseOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['status']

class AcknowledgmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['acknowledgment_date']

