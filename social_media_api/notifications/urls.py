# notifications/urls.py
from django.urls import path
from .views import NotificationListView, NotificationMarkReadView, NotificationMarkAllReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),
    path('mark-read/<int:pk>/', NotificationMarkReadView.as_view(), name='notification-mark-read'),
    path('mark-all-read/', NotificationMarkAllReadView.as_view(), name='notifications-mark-all-read'),
path('api/notifications/', include('notifications.urls')),
]
