from django.utils.timezone import now
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            user.last_login = now()
            user.save(update_fields=['last_login'])
            
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            refresh["firstname"] = user.first_name
            refresh["lastname"] = user.last_name
            refresh["isStaff"] = user.is_staff
            refresh["isSuperAdmin"] = user.is_superuser
            refresh["isActive"] = user.is_active
            refresh["role"] = user.role
            refresh["groups"] = list(user.groups.values_list("name", flat=True))
            refresh["permissions"] = list(user.user_permissions.values_list("codename", flat=True))
            user_profile = getattr(user, "userprofile", None)
            refresh["address"] = user_profile.address if user_profile else None
            refresh["phone"] = user_profile.phone if user_profile else None
            refresh["profile_picture"] = user_profile.profile_picture.url if user_profile and user_profile.profile_picture else None
            refresh["phone_number"] = user_profile.phone if user_profile else None

            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
