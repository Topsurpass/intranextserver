from .models import User, UserProfile
from .serializers import UserSerializer, UserProfileSerializer, UserFullDetailSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
# from .tasks.email_tasks import send_welcome_email
from rest_framework.response import Response
from rest_framework import status

class UserCreateView(generics.CreateAPIView):
    """Create new user account"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        user = serializer.save()
        # user = serializer.save()
        # send_welcome_email.delay(user.email, user.first_name)
        # return Response({"message": "Account created successfully. A welcome email has been sent."}, status=status.HTTP_201_CREATED)
        return Response({"message": "Account created successfully.Please sign in with your new credentials"}, status=status.HTTP_201_CREATED)

class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve single user full profile"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = "user_id"


class UserFullDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserFullDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user