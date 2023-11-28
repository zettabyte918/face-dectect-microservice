from django.urls import path
from .views import FaceDetect

urlpatterns = [
    path('detect-face/', FaceDetect.as_view(), name='face-detect'),
]