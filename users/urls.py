from django.urls import path
from .views import UserCreateView, UserProfileDetailView

userurlpatterns = [
    path('user/create/', UserCreateView.as_view(), name='user-create'),
    path("user/profile/<uuid:user_id>/", UserProfileDetailView.as_view(), name="profile_detail"),
]

