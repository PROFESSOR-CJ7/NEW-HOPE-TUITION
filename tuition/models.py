from django.db import models
from django.conf import settings


class AdminNumber(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    monthly_fee = models.PositiveIntegerField(default=getattr(settings, 'MONTHLY_FEE', 0))

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "Admin Number"
        verbose_name_plural = "Admin Numbers"


class Student(models.Model):
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.name} ({self.class_name})"

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Payment(models.Model):
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.PositiveIntegerField()
    date_paid = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='paid')
    source = models.CharField(max_length=20, default='sms')
    sms_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.parent.phone_number} → {self.amount_paid} for {self.student.name}"

    class Meta:
        ordering = ['-date_paid']
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
