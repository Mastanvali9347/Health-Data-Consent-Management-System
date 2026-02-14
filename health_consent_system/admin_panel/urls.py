from django.urls import path
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def admin_dashboard(request):
    return render(request, "admin/dashboard.html")

urlpatterns = [
    path("", user_passes_test(lambda u: u.is_authenticated and u.role == "ADMIN")(admin_dashboard), name="admin_dashboard"),
]
