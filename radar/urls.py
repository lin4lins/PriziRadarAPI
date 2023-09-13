from django.urls import path

from radar.views.login import LogIn, LogInCompleted

urlpatterns = [
    path('', LogIn.as_view(), name='login'),
    path('login-completed/', LogInCompleted.as_view(), name='login-completed'),
]
