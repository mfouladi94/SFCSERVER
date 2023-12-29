# views.py
import time
from datetime import timedelta

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from trips.models import Trip
from utils.apiResponses import *
from utils.helpers import get_estimated_delivery_time
from .models import Order, DelayReport
from .serializers import *


@method_decorator(csrf_exempt, name='dispatch')
class DelayReportApi(APIView):

    def post(self, request):
        serializer = CreateDelayReportSerializer(data=request.data)

        user = request.user

        if not serializer.is_valid():
            return APIResponse(status=NOK, messages=serializer.errors, code=CODE_Failed)

        order_id = serializer.validated_data["order_id"]

        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return APIResponse(status=NOK, messages=serializer.errors, code=CODE_Failed)

        # already reported
        already_reported = DelayReport.objects.filter(order=order, resolved=False).first()
        if already_reported:
            return APIResponse(status=NOK, messages='Your request is processing !', code=CODE_Failed)

        # Check if a trip is assigned or picked
        if order.is_delivery_past_due():
            if order.trip and order.trip.status in ['ASSIGNED', 'PICKED', 'AT_VENDOR']:

                # If a trip is assigned or picked, use  external API to estimate new delivery time
                # Provided api didn't work  , used a value to fill it
                # estimated_delivery_time = get_estimated_delivery_time(order_id)
                estimated_delivery_time = 10

                DelayReport.objects.create(order=order, estimated_delivery_time=estimated_delivery_time)
            else:
                # If no trip assigned or picked, put the order in the delay queue
                DelayReport.objects.create(order=order, is_trip_set=False)

            return APIResponse(status=OK, messages='Delay reported successfully', code=CODE_SUCCESS)
        else:
            return APIResponse(status=OK, messages='Order is processing', code=CODE_SUCCESS)


class AssignOrderToAgentView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user

        not_resolved_delay_reports = DelayReport.objects.filter(assigned_to=user, resolved=False).first()
        if not_resolved_delay_reports:
            serializer_order_data = DelayReportSerializer(not_resolved_delay_reports)
            return APIResponse(status=NOK,
                               messages='You have at least one none resolved delayed reposrt , resolve it first to continue ! ',
                               code=CODE_Failed, data=serializer_order_data.data)

        # Fetch the next order from the delay queue and assign it to an agent (FIFO)
        delay_report = DelayReport.objects.filter(assigned_to__isnull=True).order_by('timestamp').first()

        if delay_report:
            delay_report.assigned_to = request.user  # Assign the order to the current user (agent)
            delay_report.save()
            serializer_order_data = DelayReportSerializer(delay_report)
            return APIResponse(status=OK, messages='order assigned to the agent successfully', code=CODE_SUCCESS,
                               data=serializer_order_data.data)
        else:
            return APIResponse(status=NOK,
                               messages='No orders in the delay queue',
                               code=CODE_Failed)


class VendorDelayReportsApi(APIView):

    def get(self, request, vendor_id, format=None):
        user = request.user
        #vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id is None:
            return APIResponse(status=NOK,
                               messages='Need vendor_id',
                               code=CODE_Failed)

        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)
        delays = DelayReport.objects.filter(order__vendor_id=vendor_id,
                                            timestamp__range=(start_date, end_date)).order_by('-timestamp')
        serializer_order_data = DelayReportSerializer(delays, many=True)

        return APIResponse(status=OK, messages='Last week delays ', code=CODE_SUCCESS,
                           data=serializer_order_data.data)
