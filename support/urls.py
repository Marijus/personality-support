from django.urls import path

from support import views

urlpatterns = [
    path('', views.SupportView.as_view(), name='support'),
]
