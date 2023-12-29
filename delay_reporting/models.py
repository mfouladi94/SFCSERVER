from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from trips.models import Trip


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Vendor :  {self.pk} - {self.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='orders')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, blank=True, null=True)
    # TODO : define order products list
    order_time = models.DateTimeField(auto_now_add=True)
    delivery_time = models.IntegerField(default=60)

    def __str__(self):
        return f"Order {self.pk} - {self.vendor.name}"

    @property
    def estimated_delivery_time(self):
        return self.order_time + timezone.timedelta(minutes=self.delivery_time)

    def is_delivery_past_due(self):
        return timezone.now() > self.estimated_delivery_time


class DelayReport(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    is_trip_set = models.BooleanField(default=False)  # this field indicates that Trip was not assigned to the order
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.order.pk} - has trip : {self.is_trip_set} - Assigned to : {self.assigned_to} - Resolved : {self.resolved}"
