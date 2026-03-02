from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from .models import Menu, Booking
from .serializers import MenuItemSerializer, BookingSerializer, UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

# @permission_classes([IsAuthenticated])
class MenuItemView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer

class SingleMenuItemView(RetrieveUpdateAPIView, DestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


class AIHelperView(APIView):
    """Simple assistant that answers basic menu and booking questions."""

    def post(self, request, *args, **kwargs):
        prompt = (request.data.get('prompt') or '').strip()
        if not prompt:
            return Response(
                {'detail': 'The "prompt" field is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        lower_prompt = prompt.lower()
        if 'cheap' in lower_prompt or 'budget' in lower_prompt or 'affordable' in lower_prompt:
            menu_items = Menu.objects.order_by('price')[:3]
            if menu_items:
                suggestions = [f'{item.title} (${item.price})' for item in menu_items]
                message = 'Here are the most affordable menu items.'
            else:
                suggestions = []
                message = 'The menu is currently empty, so I cannot recommend affordable options yet.'
        elif 'expensive' in lower_prompt or 'premium' in lower_prompt:
            menu_items = Menu.objects.order_by('-price')[:3]
            if menu_items:
                suggestions = [f'{item.title} (${item.price})' for item in menu_items]
                message = 'Here are the premium menu items.'
            else:
                suggestions = []
                message = 'The menu is currently empty, so I cannot recommend premium options yet.'
        elif 'book' in lower_prompt or 'reservation' in lower_prompt:
            suggestions = [
                'Share your name, number of guests, and booking date.',
                'Use the /restaurant/bookings/ endpoint to create a reservation.',
            ]
            message = 'I can help with reservations. Provide your details to continue.'
        else:
            menu_count = Menu.objects.count()
            suggestions = [
                'Ask for budget recommendations (e.g. "show cheap meals").',
                'Ask for premium recommendations (e.g. "show premium meals").',
                'Ask how to create a reservation.',
            ]
            message = f'I can help with menu recommendations and bookings. Current menu items: {menu_count}.'

        return Response({'reply': message, 'suggestions': suggestions}, status=status.HTTP_200_OK)

# class UserViewSet(ModelViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#    permission_classes = [permissions.IsAuthenticated]
