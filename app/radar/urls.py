from django.urls import path

from radar import views

urlpatterns = [
    path('login/', views.LogInView.as_view(), name='login'),
    # path('random-comment/',
    #      views.InstagramPostRandomCommentView.as_view(),
    #      name='random-comment'),
]
