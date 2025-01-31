from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            response_data = {
                "message": "User created successfully",
                "status": status.HTTP_201_CREATED,
                "data": serializer.data
            }
            return Response(
                response_data, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    "error": str(e), 
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny, )
    
    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception= True)
            user = serializer.validated_data["user"]
            tokens = serializer.get_token(user)
            response_data = {
                "message": "User logged in successfully",
                "status": status.HTTP_200_OK,
                "data": serializer.data,
                "tokens": tokens
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status= status.HTTP_400_BAD_REQUEST                
            )
        
class UserListView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            queryset = self.get_queryset()
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status= status.HTTP_400_BAD_REQUEST                
            )

    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, "admin") or user.is_superuser:
                return queryset
            return queryset.filter(id=user.id)
        else:
            return queryset.none()
        
class UserDetailView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
     
    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            if request.user.id != user.id:
                return Response(
                    {
                        "message": "You do not have permission to perform this action",
                        "status": status.HTTP_403_FORBIDDEN
                    }, status= status.HTTP_403_FORBIDDEN
                )
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status= status.HTTP_400_BAD_REQUEST                
            )