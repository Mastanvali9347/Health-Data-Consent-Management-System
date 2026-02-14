from django.urls import path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .views import NotificationListView


@login_required(login_url="/auth/login/")
def notifications_page(request):
    return render(request, "patient/notifications.html")


urlpatterns = [
    path("", notifications_page, name="notifications_page"),
    path("api/", NotificationListView.as_view(), name="notifications_api"),
]
