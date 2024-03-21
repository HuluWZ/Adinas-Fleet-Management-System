from rest_framework import serializers
from accounts.models import UserAccount
from ..models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta: 
        model= Client
        fields = '__all__'
