# notifications/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import NotificationSerializer
from .models import Notification
from django.shortcuts import get_object_or_404

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')

class NotificationMarkReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()

    def get_object(self):
        obj = get_object_or_404(Notification, pk=self.kwargs['pk'], recipient=self.request.user)
        return obj

    def patch(self, request, *args, **kwargs):
        notif = self.get_object()
        notif.unread = False
        notif.save()
        return Response({'detail': 'marked read'}, status=status.HTTP_200_OK)

class NotificationMarkAllReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(recipient=request.user, unread=True).update(unread=False)
        return Response({'detail': 'all marked read'}, status=status.HTTP_200_OK)
