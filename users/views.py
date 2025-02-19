from rest_framework import viewsets
from .models import User, UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework import generics


class UserCreateView(viewsets.ModelViewSet):
    """Create, delete, retrieve and update user account"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileDetailView(generics.RetrieveAPIView):
    """Retrieve single user full profile"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = "user_id"