from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
import re

from accounts.models import Parent
from .models import Student, Payment
from .serializers import StudentSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def sms_callback(request):
    """
    Endpoint: POST /api/tuition/sms/callback/
    Body JSON:
      {
        "from": "<parent_phone>",
        "to":   "<admin_phone>",
        "text": "<amount>"
      }
    """
    sender   = request.data.get('from')
    receiver = request.data.get('to')
    body     = request.data.get('text', '')

    if receiver != settings.ADMIN_NUMBER:
        return Response({'error': 'invalid receiver'}, status=400)

    try:
        parent = Parent.objects.get(phone_number=sender)
    except Parent.DoesNotExist:
        return Response({'error': 'unknown parent'}, status=404)

    match = re.search(r'\d+', body)
    if not match:
        return Response({'error': 'no amount found'}, status=400)
    amount = int(match.group())

    student = parent.students.first()
    if not student:
        return Response({'error': 'no student linked'}, status=400)

    Payment.objects.create(
        parent      = parent,
        student     = student,
        amount_paid = amount,
        date_paid   = timezone.now(),
        status      = 'paid',
        source      = 'sms',
        sms_text    = body
    )

    return Response({
        'message': f'Recorded payment of {amount} for {student.name}'
    }, status=200)


class StudentListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/tuition/students/       → list students for the authenticated parent
    POST /api/tuition/students/       → create a new student under that parent
    """
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Student.objects.filter(parent=self.request.user)

    def perform_create(self, serializer):
        serializer.save(parent=self.request.user)


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/tuition/students/<id>/ → retrieve a student
    PUT    /api/tuition/students/<id>/ → update a student
    DELETE /api/tuition/students/<id>/ → delete a student
    """
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Student.objects.filter(parent=self.request.user)
