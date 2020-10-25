from rest_framework import serializers
from .models import User

class AccountPropertiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['pk', 'email', 'username', 'CurrentLevel', 'Profile_Pic','password']

