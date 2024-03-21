from rest_framework import serializers

from accounts.models import UserAccount
from ..models import (
    VehicleData,
    VehicleType,
    VehicleModel,
    VehicleBrand,
    VehicleColor,
    VehicleImage,
    AreaOfInterest
)

class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields =  '__all__'
                
class VehicleDataSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = VehicleData
        fields = '__all__'

    def create(self, validated_data):
        validated_data['account'] = self.context['request'].user
        return super().create(validated_data)
    
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleColor
        fields = "__all__"


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = "__all__"


class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ("image",)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = "__all__"


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = "__all__"

class AreaOfInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaOfInterest
        fields = "__all__"


class VehicleSerializer(serializers.ModelSerializer):
    images = VehicleImageSerializer(many=True, read_only=True)
    account = serializers.PrimaryKeyRelatedField(queryset=UserAccount.objects.all())
    color = ColorSerializer()
    brand = BrandSerializer()
    model = ModelSerializer()
    vehicle_type = TypeSerializer()
    area_of_interests = AreaOfInterestSerializer(many=True)

    class Meta:
        model = VehicleData
        fields = "__all__"

    def create(self, validated_data):
        images_data = self.initial_data.pop(
            "images", []
        )  # Retrieve images from initial data
        vehicle = VehicleData.objects.create(**validated_data)

        if images_data:
            for image_data in images_data:
                VehicleImage.objects.create(vehicle=vehicle, image=image_data)

        return vehicle

    def update(self, instance, validated_data):
        images_data = self.initial_data.pop(
            "images", []
        )  # Retrieve images from initial data
        instance.images.all().delete()

        for image_data in images_data:
            VehicleImage.objects.create(vehicle=instance, image=image_data)

        instance.save()
        return instance


class UpdateVehicleSerializer(serializers.ModelSerializer):
    images = VehicleImageSerializer(many=True, required=False)
    account = serializers.PrimaryKeyRelatedField(queryset=UserAccount.objects.all())
    color = serializers.PrimaryKeyRelatedField(queryset=VehicleColor.objects.all())
    brand = serializers.PrimaryKeyRelatedField(queryset=VehicleBrand.objects.all())
    model = serializers.PrimaryKeyRelatedField(queryset=VehicleModel.objects.all())
    vehicle_type = serializers.PrimaryKeyRelatedField(
        queryset=VehicleType.objects.all()
    )

    class Meta:
        model = VehicleData
        fields = "__all__"

    def update(self, instance, validated_data):
        images_data = self.context["request"].FILES.getlist(
            "images"
        )  # Get uploaded files
        print(images_data)
        print(instance.images.all())
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if images_data:
            instance.images.all().delete()
            for image_data in images_data:
                VehicleImage.objects.create(vehicle=instance, image=image_data)
        print(" No")
        instance.save()
        return instance


class VehicleRegisterSerializer(serializers.ModelSerializer):
    libre = serializers.FileField(required=False)
    license = serializers.FileField(required=False)

    class Meta:
        model = VehicleData
        fields = [
            "plate_number",
            # "area_of_interests",
            "color",
            "transmission",
            "fuel_type",
            "driver_status",
            "price_per_day",
            "vehicle_type",
            "libre",
            "license",
            "brand",
            "model",
            "production_year",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        try:
            user_account = UserAccount.objects.get(pk=user.id)
            print(user_account)
        except UserAccount.DoesNotExist:
            raise serializers.ValidationError(
                "UserAccount not found for the authenticated user."
            )

        validated_data["account"] = user_account
        vehicle = VehicleData.objects.create(**validated_data)
        vehicle.created_by = user_account
        return vehicle
