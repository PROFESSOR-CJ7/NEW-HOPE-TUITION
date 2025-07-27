from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("""
        <h2>🎓 Welcome to NewHope Tuition API</h2>
        <p>This API powers SMS-based tuition management for parents and admins.</p>
        <ul>
            <li><a href="/admin/">Admin Panel</a></li>
            <li><a href="/api/auth/">Authentication Endpoints</a></li>
            <li><a href="/api/tuition/students/">Student Management</a></li>
            <li><a href="/api/tuition/payments/">Payment Records</a></li>
            <li><a href="/api/tuition/sms/callback/">SMS Callback Endpoint</a></li>
        </ul>
        <p>© NewHope Backend | Powered by Django 💻</p>
    """, content_type="text/html")

urlpatterns = [
    path('', home),  # Homepage on root URL
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/tuition/', include('tuition.urls')),
]
