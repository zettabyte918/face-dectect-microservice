from django.urls import path
from .views import SendSMSView

urlpatterns = [
    path('send/', SendSMSView.as_view(), name='send_sms'),
]