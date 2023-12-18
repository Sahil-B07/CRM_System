from django.urls import include, path
from rest_framework import routers
from api import views 

router = routers.DefaultRouter()
router.register(r'vendors', views.VendorViewSet)
router.register(r'purchase_orders', views.PurchaseOrderViewSet)
router.register(r'performance', views.MetricsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('purchase_orders/<int:pk>/acknowledge/', views.PurchaseOrderViewSet.as_view({'get': 'acknowledge_url'}), name='purchaseorder-acknowledge-update'),
]
