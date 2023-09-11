from django.urls import path

from radar.views.login import LogIn, Home

urlpatterns = [
    path('', LogIn.as_view(), name='login'),
    path('home/<str:code_verifier>', Home.as_view(), name='home'),
]
