from django.urls import path
from .views import (
    CreateBookingView, 
    PayBookingView,
    ConfirmPaymentView,
    BookingDetailView, 
    BookingListView, 
    BookingCancelView,
    BookingUpdateView,
)


urlpatterns = [
    path('create/', CreateBookingView.as_view(), name="create_booking"),
    path('<uuid:booking_id>/pay/',  PayBookingView.as_view(), name="payment"),
    path('<uuid:booking_id>/confirm_payment/',  ConfirmPaymentView.as_view(), name="confirm_payment"),
    path('<uuid:booking_id>/', BookingDetailView.as_view(), name="booking_detail"),
    path('<uuid:booking_id>/cancel/', BookingCancelView.as_view(), name="booking_cancelled"),
    path('<uuid:booking_id>/update/', BookingUpdateView.as_view(), name="booking_update"),
    path('list/', BookingListView.as_view(), name="bookings_list"),
]