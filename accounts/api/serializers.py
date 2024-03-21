from rest_framework import serializers
from ..models import UserAccount


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = (
            "first_name",
            "last_name",
            "gender",
            "address",
            "phone_number",
            "profile_image",
        )

    def validate(self, data):
        phone_number = data.get("phone_number")
        email = data.get("email")

        if UserAccount.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("Phone number already exists.")

        if email and UserAccount.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")
        return data

    def update(self, instance, validated_data):
        for field in self.Meta.fields:
            setattr(
                instance, field, validated_data.get(field, getattr(instance, field))
            )

        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "gender",
            "address",
            "profile_image",
            "is_driver",
            "is_client",
            "is_owner",
            "is_both",
        ]


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = (
            "first_name",
            "last_name",
            "gender",
            "address",
            "username",
            "email",
            "phone_number",
            "profile_image",
            'is_driver',
            'is_owner',
            'is_both'
        )

    def validate(self, data):
        phone_number = data.get("phone_number")
        email = data.get("email")

        if UserAccount.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("Phone number already exists.")

        # Check if the email is provided and already exists
        if email and UserAccount.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")

        return data


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = (
            "first_name",
            "last_name",
            "gender",
            "profile_image",
            "address",
            "username",
            "email",
            "phone_number",
        )
