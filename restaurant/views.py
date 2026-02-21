from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from .models import Menu, Booking
from .serializers import MenuItemSerializer, BookingSerializer, UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Min, Max

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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ai_instrumantel(request):
    """
    Lightweight AI-style menu insights endpoint.
    """
    stats = Menu.objects.aggregate(
        average_price=Avg('price'),
        lowest_price=Min('price'),
        highest_price=Max('price'),
    )
    total_items = Menu.objects.count()

    if total_items == 0:
        recommendation = 'Add your first menu item to unlock AI insights.'
    elif stats['average_price'] and stats['average_price'] > 25:
        recommendation = 'Consider adding a budget-friendly option to improve balance.'
    else:
        recommendation = 'Menu pricing looks accessible. Consider adding a premium special item.'

    payload = {
        'feature': 'ai-instrumantel',
        'total_items': total_items,
        'average_price': stats['average_price'],
        'price_range': {
            'lowest': stats['lowest_price'],
            'highest': stats['highest_price'],
        },
        'recommendation': recommendation,
    }
    return Response(payload, status=status.HTTP_200_OK)

# class UserViewSet(ModelViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#    permission_classes = [permissions.IsAuthenticated]
