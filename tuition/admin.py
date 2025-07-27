# tuition/admin.py

from django.contrib import admin
from .models import AdminNumber, Student, Payment

@admin.register(AdminNumber)
class AdminNumberAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'monthly_fee')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_name', 'parent')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('parent', 'student', 'amount_paid', 'date_paid', 'status')
