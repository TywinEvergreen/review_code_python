from django.urls import path

from transfer.views import TransferAPIView

urlpatterns = [
    # url() устарело в Django 2.0
    path('', TransferAPIView.as_view(), name='transfer'),
]

