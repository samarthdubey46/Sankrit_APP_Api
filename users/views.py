from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serelizers import AccountPropertiesSerializer
from .models import User
from rest_framework.authtoken.models import Token


class AllinOne(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AccountPropertiesSerializer


@api_view(['POST'])
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = User.objects.filter(email=email, password=password)[0]
    s = Token.objects.get(user=user)
    return Response({'token': s.key})


class LeaderBoard(ListAPIView):
    queryset = User.objects.all()
    serializer_class = AccountPropertiesSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ['username', 'CurrentLevel']
