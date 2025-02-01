from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .serializers import BookingSerializer
from rest_framework.decorators import action
from django.conf import settings
import requests
import uuid 
from .models import Booking
from rest_framework.views import APIView
from .utils import initiate_payment

class CreateBookingView(GenericAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:

            serializer = self.get_serializer(data = request.data)
            serializer.is_valid(raise_exception= True)   
            serializer.save()
            booking_id = serializer.data["id"]
            pay_url = f'http://localhost:8000/api/v1/bookings/{booking_id}/pay/'
            return Response(
                {
                    "message": "Booking created Successfully",
                    "status": status.HTTP_201_CREATED,
                    "data": serializer.data,
                    "pay_url": pay_url
                }, status= status.HTTP_201_CREATED
            ) 
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST,
                }, status= status.HTTP_400_BAD_REQUEST
            )
        
class PayBookingView(APIView):
    #serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request,booking_id, *args, **kwargs):
        try:

            booking = Booking.objects.get(id=booking_id)
            amount = booking.amount
            email = request.user.email
            name = request.user.username
            phonenumber = request.user.phone_number
            booking_id = booking.id
            redirect_url = f'http://localhost:8000/api/v1/bookings/{booking_id}/confirm_payment/'

            return initiate_payment(amount, email, name,phonenumber, redirect_url)
        except Booking.DoesNotExist:
            return Response(
                {
                    "message": "Booking Not Found",
                    "status": status.HTTP_404_NOT_FOUND
                }, status= status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST,
                }, status= status.HTTP_400_BAD_REQUEST
            )
        
class ConfirmPaymentView(GenericAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id,  *args, **kwargs):
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.status = 'PAID'
            booking.save()
            serializer = self.get_serializer(booking)
            return Response(
                {
                    "message": "Payment Confirmed",
                    "status": status.HTTP_200_OK,
                    "data":serializer.data
                }, status= status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST,
                }, status= status.HTTP_400_BAD_REQUEST
            )
        
class BookingDetailView(GenericAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id, *args, **kwargs):
        try:

            user = request.user
            booking = Booking.objects.get(id=booking_id)
            serializer = self.get_serializer(booking)
            if booking.user != user:
                return Response(
                    {
                        "message": "You do not have permission to do this",
                        "status": status.HTTP_403_FORBIDDEN
                    }, status=status.HTTP_403_FORBIDDEN
                )
            return Response(
                {
                    "message": "Book retrieved succesfully",
                    "data": serializer.data,
                    "status": status.HTTP_200_OK
                }, status=  status.HTTP_200_OK
            )
        except Booking.DoesNotExist:
            return Response(
                {
                    "message": "Booking not found",
                    "status": status.HTTP_404_NOT_FOUND
                }, status= status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST,
                }, status= status.HTTP_400_BAD_REQUEST
            )
        
class BookingListView(GenericAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()

    def get(self, request):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "message": "Bookings Retrieved successfully",
                    "status": status.HTTP_200_OK,
                    "data": serializer.data
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST,
                }, status= status.HTTP_400_BAD_REQUEST
            )    

    def  get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if hasattr(user, "admin") or user.is_superuser:
            return queryset
        return queryset.filter(user=user)  
    
class BookingCancelView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
            if booking.status != "PENDING":
                return Response(
                    {
                        "message": "You cannot cancel the booking",
                        "data": f"Your booking status is {booking.status}",
                        "status": status.HTTP_403_FORBIDDEN
                    }, status=  status.HTTP_403_FORBIDDEN
                )
            booking.status = 'CANCELLED'
            booking.save()
            return Response(
                {
                    "message": "Booking cancelled succesfully",
                    "status": status.HTTP_200_OK,
                    "data": {
                        "id": booking.id,
                        "status": booking.status
                    }
                }, status=status.HTTP_200_OK
            )
        except Booking.DoesNotExist:
            return Response(
                {
                    "message": "Booking Not Found",
                    "status": status.HTTP_404_NOT_FOUND
                }, status=  status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST,
                }, status= status.HTTP_400_BAD_REQUEST
            )  

class BookingUpdateView(GenericAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


    def put(self, request, booking_id):
        try:
            booking = Booking.objects.get(id= booking_id)
            if booking.status != "PENDING":
                return Response(
                    {
                        "message": "You cannot cancel the booking",
                        "data": f"Your booking status is {booking.status}",
                        "status": status.HTTP_403_FORBIDDEN
                    }, status=  status.HTTP_403_FORBIDDEN
                )                
            serializer = self.get_serializer(booking, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "Booking updated succesfully",
                    "status": status.HTTP_200_OK,
                    "data":serializer.data
                }, status= status.HTTP_200_OK
            )
        except Booking.DoesNotExist:
            return Response(
                {
                    "message": "Booking Not Found",
                    "status": status.HTTP_404_NOT_FOUND
                }, status=  status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                    "status": status.HTTP_400_BAD_REQUEST,
                }, status= status.HTTP_400_BAD_REQUEST
            )