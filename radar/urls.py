from rest_framework.routers import DefaultRouter

from radar import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'ig-accounts', views.InstagramAccountViewSet, basename='ig-account')

urlpatterns = router.urls
