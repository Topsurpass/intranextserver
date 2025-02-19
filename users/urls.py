from django.urls import path, include
from rest_framework import routers
from .views import UserCreateView, UserProfileDetailView

router = routers.DefaultRouter()
router.register(r'users', UserCreateView, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path("user/profile/<uuid:user_id>/", UserProfileDetailView.as_view(), name="profile_detail"),
]

