from django.urls import path
from radar import views

urlpatterns = [
    path('login/', views.LogInView.as_view(), name='login'),
    path('post', views.PostGetView.as_view(), name='view-post'),
    # path('random-comment/',
    #      views.InstagramPostRandomCommentView.as_view(),
    #      name='random-comment'),
]
