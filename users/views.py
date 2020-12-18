from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serelizers import AccountPropertiesSerializer


class AllinOne(ModelViewSet):
    queryset = User.objects.filter(is_superuser=False)
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = AccountPropertiesSerializer


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = User.objects.filter(email=email, )
    if len(user) <= 0:
        return Response({'status': False, 'res': f'No User With this {email}'})
    user = user[0]
    if not user.check_password(password):
        return Response({'status': False, 'res': f'The Password Is Invalid'})
    userData = AccountPropertiesSerializer(instance=user)
    s = Token.objects.get(user=user)
    obj = {'token': s.key, 'status': True}
    for i, j in userData.data.items():
        obj[i] = j
    return Response(obj)


@api_view(['POST'])
def register(request):
    obj = {'errors': []}
    email = ''
    username = ''
    password = ''
    Profile_Pic = ''
    if 'email' not in request.data.keys():
        obj['errors'].append({'email': 'Enter Email'})
    else:
        email = request.data.get('email')
    if 'password' not in request.data.keys():
        obj['errors'].append({'password': 'Enter Password'})
    else:
        password = request.data.get('password')
    if 'username' not in request.data.keys():
        obj['errors'].append({'username': 'Enter Username'})
    else:
        username = request.data.get('username')
    if 'Profile_Pic' not in request.data.keys():
        obj['errors'].append({'Profile_Pic': 'Enter Profile_Pic'})
    else:
        Profile_Pic = request.data.get('Profile_Pic')
    if len(obj['errors']) > 0:
        return Response({'status': False, 'errors': obj['errors'], 'message': 'Invalid Data'})
    user_test = User.objects.filter(email=email)
    print(user_test)
    if len(user_test) >= 1:
        return Response({'status': False, 'message': 'user with this email already exists'})
    user = User.objects.create_user(email, username, password=password, profile=Profile_Pic)
    return Response({'status': True, 'message': 'User Registered, now you can login'})




class LeaderBoard(ListAPIView):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = AccountPropertiesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ['username', 'CurrentLevel']


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def getTop(request):
    users = User.objects.filter(is_superuser=False)
    Users_Final = []
    for i in users:
        Users_Final.append(AccountPropertiesSerializer(instance=i).data)
    Users_Final.sort(key=lambda x: x['CurrentLevel'], reverse=True)
    return Response(Users_Final[:10])
