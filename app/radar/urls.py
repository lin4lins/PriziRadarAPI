from django.urls import path

from radar import views

urlpatterns = [
    path('connection/', views.ConnectionCreateView.as_view(), name='connection-create'),
    # path('random-comment/',
    #      views.InstagramPostRandomCommentView.as_view(),
    #      name='random-comment'),
]
