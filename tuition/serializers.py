# tuition/serializers.py

from rest_framework import serializers
from django.conf import settings
from .models import AdminNumber, Student, Payment


class AdminNumberSerializer(serializers.ModelSerializer):
    """
    Serializer for AdminNumber model.
    """
    class Meta:
        model = AdminNumber
        fields = ['id', 'phone_number', 'monthly_fee']


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for Student model.
    - parent: read-only PK of Parent
    - parent_phone: read-only phone_number of Parent
    """
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    parent_phone = serializers.CharField(source='parent.phone_number', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'class_name', 'parent', 'parent_phone']


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payment model.
    - parent: read-only PK of Parent
    - parent_phone: read-only phone number of Parent
    - student_name: read-only name of Student
    """
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    parent_phone = serializers.CharField(source='parent.phone_number', read_only=True)
    student_name = serializers.CharField(source='student.name', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'parent',
            'parent_phone',
            'student',
            'student_name',
            'amount_paid',
            'date_paid',
            'status',
            'source',
            'sms_text',
        ]
        read_only_fields = ['date_paid', 'parent', 'parent_phone', 'student_name']
