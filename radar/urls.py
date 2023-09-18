from rest_framework.routers import DefaultRouter

from radar import views

router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename="user")
urlpatterns = router.urls
