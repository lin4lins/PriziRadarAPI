from django.urls import path

from radar.views.login import AuthorizationView

urlpatterns = [
    path('', AuthorizationView.as_view(), name='auth'),
]
