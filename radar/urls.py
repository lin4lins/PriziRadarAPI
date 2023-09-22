from rest_framework.routers import DefaultRouter

from radar import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'ig-accounts',
                views.InstagramAccountViewSet,
                basename='ig-account')
router.register(r'ig-posts', views.InstagramPostViewSet, basename='ig-post')

urlpatterns = router.urls
