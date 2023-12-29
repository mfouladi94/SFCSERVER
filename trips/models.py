from django.db import models

class Trip(models.Model):
    DELIVERED = 'DELIVERED'
    PICKED = 'PICKED'
    VENDOR_AT = 'AT_VENDOR'
    ASSIGNED = 'ASSIGNED'

    STATUS_CHOICES = [
        (DELIVERED, 'Delivered'),
        (PICKED, 'Picked'),
        (VENDOR_AT, 'Vendor At'),
        (ASSIGNED, 'Assigned'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
