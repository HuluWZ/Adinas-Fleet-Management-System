from rest_framework import serializers
from ..models import Owner ,Driver
from accounts.models import UserAccount
from accounts.api.serializers import UserSerializer,UserSignupSerializer ,UserAccountSerializer

class OwnerSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=['driver', 'owner', 'both'])
    class Meta:
        model = UserAccount
        fields = ('role','first_name', 'last_name','gender',
                    'address',
                  'username', 'email', 'phone_number','profile_image')  

    def validate(self, data):
        phone_number = data.get('phone_number')
        email = data.get('email')

        if UserAccount.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("Phone number already exists.")

        if email and UserAccount.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")

        return data
    def create(self, validated_data):
        role = validated_data.pop('role')
        user_account_instance = UserAccount.objects.create(**validated_data)
        if role == 'driver':
            user_account_instance.is_driver = True
        elif role == 'owner':
            user_account_instance.is_owner = True
        elif role == 'both':
            user_account_instance.is_both = True
        
        user_account_instance.save()

        owner_instance = Owner.objects.create(
            account=user_account_instance,
            created_by=user_account_instance
        )

        return owner_instance
    
class DriverSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=['driver', 'owner', 'both'])
    class Meta:
        model = UserAccount
        fields = ('role','first_name', 'last_name','gender',
                    'address',
                  'username', 'email', 'phone_number','profile_image')  

    def validate(self, data):
        phone_number = data.get('phone_number')
        email = data.get('email')

        if UserAccount.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("Phone number already exists.")

        if email and UserAccount.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")

        return data
    def create(self, validated_data):
        role = validated_data.pop('role')
        user_account_instance = UserAccount.objects.create(**validated_data)
        if role == 'driver':
            user_account_instance.is_driver = True
        elif role == 'owner':
            user_account_instance.is_owner = True
        elif role == 'both':
            user_account_instance.is_both = True
        
        user_account_instance.save()

        owner_instance = Owner.objects.create(
            account=user_account_instance,
            created_by=user_account_instance
        )

        return owner_instance
        

class OwnerRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Owner
        fields= '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        print(" User ",user)
        try:
            user_account = UserAccount.objects.get(pk=user.id)
        except UserAccount.DoesNotExist:
            raise serializers.ValidationError("UserAccount not found for the authenticated user.")
        
        validated_data['account'] = user_account
        
        return Owner.objects.create(**validated_data)
