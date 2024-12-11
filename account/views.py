
from rest_framework.response import Response
from django.middleware import csrf
from .models import User
from .serializer import User_Registration_Serializer, User_Login_serializer,User_Serializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .customThrottleuser import CustomAnonRateThrottleUser
from rest_framework import status
# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    throttle_classes = [CustomAnonRateThrottleUser]
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        # print(request)
        serializer = User_Registration_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    throttle_classes = [CustomAnonRateThrottleUser]
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = User_Login_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                token = get_tokens_for_user(user)
                instance = get_object_or_404(User, email=email)
                serializer = User_Serializer(instance)

                data = {
                    "data": serializer.data

                }
                response = Response(data, status=status.HTTP_200_OK)
                response.set_cookie(key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                                    value=token["access"],
                                    domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
                                    path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
                                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                    secure=False,
                                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                                    )
                response.set_cookie(key=settings.SIMPLE_JWT['Auth_COOKIE_REFRESH'],
                                    value=token["refresh"],
                                    domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
                                    expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                                    )

                csrf.get_token(request)
                return response
            else:
                return Response({"error": "Invalid username or password!!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid username or password!!"}, status=status.HTTP_400_BAD_REQUEST)