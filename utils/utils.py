def onTimeDelivery(vendors_purchase_orders, pk, models):
    total_completed_POs = vendors_purchase_orders.filter(
        vendor_id=pk, status='Completed').count()
    completed_POs = vendors_purchase_orders.filter(vendor_id=pk).filter(
        models.Q(date_updated__lte=models.F('delivery_date'))).count()

    try:
        on_time_delivery = completed_POs/total_completed_POs
    except:
        on_time_delivery = 0.0

    return on_time_delivery


def qualityRate(vendors_purchase_orders, pk, models, metrics):
    quality_rating__avg = vendors_purchase_orders.filter(vendor_id=pk).aggregate(
        models.Avg('quality_rating'))['quality_rating__avg']
    
    return quality_rating__avg


def avgResponseTime(vendors_purchase_orders, pk, models):
    avg_resp = vendors_purchase_orders.filter(vendor_id=pk).annotate(
        date_diff=models.ExpressionWrapper(
            models.F('acknowledgment_date') - models.F('issue_date'),
            output_field=models.fields.DurationField()
        )
    )
    average_date_diff_seconds = avg_resp.aggregate(
        avg_date_diff=models.Avg('date_diff'))['avg_date_diff'].total_seconds()

    return average_date_diff_seconds


def fulfilmentRate(vendors_purchase_orders, pk):
    completed_POs = vendors_purchase_orders.filter(
        vendor_id=pk, status='Completed').count()
    total_POs = vendors_purchase_orders.filter(vendor_id=pk).count()

    try:
        fulfilment_rate = completed_POs / total_POs
    except:
        fulfilment_rate = 0.0
    return fulfilment_rate
