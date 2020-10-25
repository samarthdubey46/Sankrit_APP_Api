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
import rest_framework.permissions as permissions
from rest_framework.authtoken.models import Token


class AllinOne(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = AccountPropertiesSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [permissions.AllowAny, ]
        else:
            self.permission_classes = [permissions.IsAuthenticated, ]
        return super(self.__class__, self).get_permissions()


@api_view(['POST'])
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = User.objects.filter(email=email, password=password)
    print(type(user))
    if len(user) <= 0:
        return Response({'status': False, 'res': f'No User With this {email}'})

    user = user[0]
    s = Token.objects.get(user=user)
    return Response({'token': s.key, 'status': True})


class LeaderBoard(ListAPIView):
    queryset = User.objects.all()
    serializer_class = AccountPropertiesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ['username', 'CurrentLevel']
