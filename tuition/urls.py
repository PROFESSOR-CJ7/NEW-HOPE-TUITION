from django.urls import path
from .views import (
    sms_callback,
    StudentListCreateView,
    StudentDetailView,
)

urlpatterns = [
    path('sms/callback/', sms_callback, name='sms_callback'),
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    path('students/<int:id>/', StudentDetailView.as_view(), name='student-detail'),
]
