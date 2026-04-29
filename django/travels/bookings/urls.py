
from django.urls import path
from .views import RegisterView, LoginView, BusListcreateView,BusDetailView,UserBookingsView,Bookingview

urlpatterns = [
    path('buses/', BusListcreateView.as_view(), name='buslist'),
    path('buses/<int:pk>/',BusDetailView.as_view(),name ="bus-detail" ),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/<int:user_id>/bookings/', UserBookingsView.as_view(), name='user-bookings'),
    path('booking/', Bookingview.as_view(), name='bookings'),
]