from django.urls import path
from radar import views

urlpatterns = [
    path('login/', views.LogInView.as_view(), name='login'),
    path('post', views.PostView.as_view(), name='post'),
    path('post/<int:id>/random-comment', views.RandomCommentView.as_view(), name='random-comment')
]
