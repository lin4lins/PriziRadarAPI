from django.urls import path

from radar import views

urlpatterns = [
    path('users/', views.UserCreateView.as_view(), name="user-create"),
    path('users/me/', views.UserRetrieveView.as_view(), name="user-retrieve"),
    path('ig-accounts/', views.InstagramAccountCreateView.as_view(), name = 'ig-account-create'),
]
