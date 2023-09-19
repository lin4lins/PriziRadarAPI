from django.urls import path

from radar import views

router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename="user")
urlpatterns = router.urls
urlpatterns = [
    path('users/', views.UserCreateView.as_view(), name="user-create"),
    path('users/me/', views.UserRetrieveView.as_view(), name="user-retrieve"),
]
