from django.urls import path, include
from rest_framework.routers import DefaultRouter

from radar import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'ig-accounts',
                views.InstagramAccountViewSet,
                basename='ig-account')

urlpatterns = [
    path('', include(router.urls)),
    path('random-comment/',
         views.InstagramPostRandomCommentView.as_view(),
         name='random-comment'),
]
