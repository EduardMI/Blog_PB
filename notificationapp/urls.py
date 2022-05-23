from django.urls import path

from .views import NotificationListVew, NotificationIsReadVew

app_name = 'notificationapp'

urlpatterns = [
    path('all/<int:pk>/', NotificationListVew.as_view(), name='notify_all'),
    path('delete/<int:pk>', NotificationIsReadVew.as_view(), name='notify_delete'),
]
