from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from core.custom_auth import EmailNameAuthBackend
from rest_framework.response import Response
from .signals import send_verification_email
from .serializers import UserSerializer

# Create your views here.


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["name"] = user.name
        token["email"] = user.email
        
        return token

class CustomTokenObtain(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = EmailNameAuthBackend.authenticate(email, password)
        if user is not None:
            if user.is_email_verified:
                if user.is_active:
                    refresh = RefreshToken.for_user(user)
                    token = {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                    return Response(token, status=status.HTTP_200_OK)
                return Response({'error': 'Account disabled!'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                send_verification_email(user)
                return Response({'error': 'Account not verified!'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': 'Invalid login Details'}, status=status.HTTP_401_UNAUTHORIZED)


class UserRegistrationView(generics.GenericAPIView):
    serializer_class = UserSerializer
    def post(self, request,*args,**kwargs):
        req = request.data.copy()
        data = req['data']
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer = serializer.save()
            message = {'message':f'Account created succesffuly!'}
            return Response({message,serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

   
