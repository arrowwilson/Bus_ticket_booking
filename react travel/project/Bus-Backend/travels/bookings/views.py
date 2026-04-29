

# authicate,permission,token,status,response,APIView,generics

from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status,generics
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer,BusSerializer,BookingSerializer
from rest_framework.response import Response
from .models import Bus,Seat,Booking




class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user :
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id # type: ignore
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class BusListcreateView(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class BusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer


class Bookingview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Seat_id = request.data.get('seat')

        try:
            seat = Seat.objects.get(id=Seat_id)
            if seat.is_booked:
                return Response({'error': 'Seat is already booked'}, status=status.HTTP_400_BAD_REQUEST)
            seat.is_booked = True
            seat.save()

            booking = Booking.objects.create(
                user=request.user,
                bus =seat.bus,
                seat=seat   
            )
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Seat.DoesNotExist:
            return Response({'error': 'Invalid seat ID'}, status=status.HTTP_400_BAD_REQUEST)
class UserBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,user_id):
        if request.user.id != user_id:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        bookings = Booking.objects.filter(user_id=user_id)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

     
        

    
            
        