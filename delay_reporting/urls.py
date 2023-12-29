
from django.urls import path
from .api import *

urlpatterns = [
    path('delay-reports/', DelayReportApi.as_view(), name='delay-report-create'),
    path('assign-order/', AssignOrderToAgentView.as_view(), name='assign-order-to-agent'),
    path('vendor-delay-reports/<int:vendor_id>/', VendorDelayReportsApi.as_view(), name='vendor-delay-reports'),
]
