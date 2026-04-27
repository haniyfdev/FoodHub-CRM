from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import *


# -- -- -- -- -- -- -- -- -- --
class LoginRateThrottle(AnonRateThrottle):
    scope = 'login'

# -- -- -- -- -- -- -- -- -- --
class RegisterView(APIView):
    permission_classes     = [AllowAny]
    authentication_classes = []

    def get(self, request):
        return Response({'message': "M'alumotlarni POST orqali yuboring"})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        # user'dan kelgan json'dan --> python obj

        if serializer.is_valid(): # pyobj'ni validation qilamiz
            user       = serializer.save() # created user obj (raw)
            # restaurant = Restaurant.objects.first()
            # if restaurant:
            #     Profile.objects.create(user=user, restaurant=restaurant)
            # else:
            #     pass
            # profile    = Profile.objects.create(user=user, restaurant=restaurant)

            refresh = RefreshToken.for_user(user)
            # user'ni ma'lumotlari bilan refresh token generation bo'layapti

            return Response({
                'message': 'Succes your Log-In !',
                'tokens': {
                    'access': str(refresh.access_token),
                 # .access_token deganda refresh tokendan user_id'ni olib darxol access_token yasaydi
                    'refresh': str(refresh),
                },
                'user': {
                    'id':       user.id,
                    'username': user.username,
                    'email':    user.email,
                }# py.obj -> json
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# -- -- -- -- -- -- -- -- -- --
class LoginView(TokenObtainPairView):
    serializer_class = MytokenObtainPairSerializer
    throttle_classes = [LoginRateThrottle]
    permission_classes = [AllowAny]

# -- -- -- -- -- -- -- -- -- --
class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token yuborilmadi'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            # user'dan kelgan tokenni yana py.object'ga aylantiramiz
            token.blacklist() # keyin o'sha token'ni qora royxatga qo'shamiz

            return Response({'message': 'SuccesFuly Log-Out'})

        except Exception as e:
            return Response(
                {'error': f"Tokenda xatolik: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
# -- -- -- -- -- -- -- -- -- --
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        serializer = UserSerializer(request.user)
        # .user - bu User modelidagi row nomi 
        return Response(serializer.data)
        # bu yerda ham py.obj -> json bo'layapti
