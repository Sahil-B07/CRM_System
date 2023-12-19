from django.urls import reverse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, decorators, response

from .models import *
from .serializers import *
from utils.utils import onTimeDelivery, qualityRate, avgResponseTime, fulfilmentRate


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @decorators.action(detail=True, methods=['GET'])
    def performance(self, request, pk=None):
        vendor = Vendor.objects.filter(pk=pk).first()
        vendors_purchase_orders = PurchaseOrder.objects

        try:
            on_time_delivery = onTimeDelivery(vendors_purchase_orders, pk, models)
            quality_rate = qualityRate(
                vendors_purchase_orders, pk, models, Metrics)
            avg_response_time = avgResponseTime(
                vendors_purchase_orders, pk, models)
            fulfilment_rate = fulfilmentRate(vendors_purchase_orders, pk)
        except:
            return response.Response({'Message':'No Purchase Order(s) found for this Vendor!'})

        metrics_instance, created = Metrics.objects.update_or_create(
            vendor=vendor,
            defaults={'on_time_delivery_rate': on_time_delivery, 'quality_rating_avg': quality_rate,
                      'average_response_time': avg_response_time, 'fulfilment_rate': fulfilment_rate}
        )

        # also update the initial/recent vendors records created/updated
        Vendor.objects.update_or_create(
            id=pk,
            defaults={'on_time_delivery_rate': on_time_delivery, 'quality_rating_avg': quality_rate,
                      'average_response_time': avg_response_time, 'fulfilment_rate': fulfilment_rate}
        )

        serializer = MetricSerializer(
            metrics_instance, context={'request': request})
        return response.Response(serializer.data)


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()

    def get_serializer_class(self):
        if self.action == 'acknowledge':
            return AcknowledgmentUpdateSerializer
        elif self.action == 'update':
            return PurchaseOrderUpdateSerializer
        return POSerializer
    
    @decorators.action(detail=True, methods=['GET','PUT'])
    def acknowledge(self, request, pk=None):
        instance = self.get_object()
        serializer = AcknowledgmentUpdateSerializer(instance)
        
        if request.method == 'PUT':
            serializer = AcknowledgmentUpdateSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data)
            else:
                return response.Response(serializer.errors, status=response.status.HTTP_400_BAD_REQUEST)
        else:
            return response.Response({'acknowledgment_date': serializer.data.get('acknowledgment_date')})
        
class MetricsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Metrics.objects.all()
    serializer_class = MetricSerializer
