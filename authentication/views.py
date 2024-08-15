from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from authentication.serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login(request):
    user = get_object_or_404(User, username=request.data["username"])

    if not user.check_password(request.data["password"]):
        return Response(
            {"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED
        )

    token = CustomTokenObtainPairSerializer.get_token(user)
    user_serializer = UserSerializer(instance=user)

    return Response(
        {
            "refresh": str(token),
            "access": str(token.access_token),
            "user": user_serializer.data,
        }
    )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data["password"])
        user.save()

        token = CustomTokenObtainPairSerializer.get_token(user)

        return Response(
            {
                "refresh": str(token),
                "access": str(token.access_token),
                "user": serializer.data,
            }
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def test_token(request):
    user = request.user
    token = CustomTokenObtainPairSerializer.get_token(user)
    user_serializer = UserSerializer(instance=user)
    return Response(
        {
            "refresh": str(token),
            "access": str(token.access_token),
            "user": user_serializer.data,
        }
    )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def refresh_token(request):
    refresh_token = request.data.get("refresh")

    if not refresh_token:
        return Response(
            {"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        token = RefreshToken(refresh_token)
        user_id = token["user_id"]
        user = User.objects.get(id=user_id)
        token = CustomTokenObtainPairSerializer.get_token(user)
        user_serializer = UserSerializer(instance=user)
        return Response(
            {
                "refresh": str(token),
                "access": str(token.access_token),
                "user": user_serializer.data,
            }
        )
    except (InvalidToken, TokenError) as e:
        return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
