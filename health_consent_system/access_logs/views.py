from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import AccessLog
from .serializers import AccessLogSerializer


@login_required(login_url="/auth/login/")
def access_logs_page(request):
    if request.user.role == "ADMIN":
        logs = AccessLog.objects.all()
    else:
        logs = AccessLog.objects.filter(user=request.user)

    return render(
        request,
        "admin/logs.html",
        {"logs": logs}
    )


class MyAccessLogsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "ADMIN":
            logs = AccessLog.objects.all()
        else:
            logs = AccessLog.objects.filter(user=request.user)

        serializer = AccessLogSerializer(logs, many=True)
        return Response(serializer.data)
