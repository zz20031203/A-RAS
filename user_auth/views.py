from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate
from .models import UserProfile

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            print(serializer.validated_data)
            user = serializer.save()
            return Response({"status": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)  # 调试输出
            tel = serializer.validated_data['phone']
            password = serializer.validated_data['password']
            #print()
            user=UserProfile.objects.get(tel=tel)
            #user = authenticate(username=tel, password=password)
            if user is not None:
                # 登录成功的处理逻辑
                return Response({"status": "Login successful"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
