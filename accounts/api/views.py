import json
from django.http import QueryDict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import pyotp

from accounts.authentication import JWTAuthentication
from utils.sms_messages import sms_api_router

from ..models import UserAccount
from .serializers import UserSignupSerializer, UserSerializer, UserUpdateSerializer
from vehicle.models import VehicleData
from booking.models import VehicleBooking, AssignedVehicle

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token


class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSignupView(APIView):

    def post(self, request):
        try:
            print(request.data)
            serializer = UserSignupSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()  # Save the user
                serialized_user = UserSerializer(user)
                user.otp_counter += 1  # Update Counter At every Call

                key = pyotp.random_base32()

                user.otp_secret = key
                user.save()
                otp_token = pyotp.TOTP(key)
                sms_api_router(user.phone_number,'Your Adinas Car Rent App verification OTP is {}'.format(
                            otp_token.at(user.otp_counter)))
                return Response(
                    {"message": "User created successfully", "user": serialized_user.data},
                    status=status.HTTP_201_CREATED,
                ) 
            return Response({"message":serializer.errors['non_field_errors'][0]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginInitiateView(APIView):
    def post(self, request):
        print(request.data)
        phone_number = request.data["phone_number"]
        print(phone_number)
        try:
            otp_secret = pyotp.random_base32()
            user = UserAccount.objects.get(phone_number=phone_number)
            user.otp_secret = otp_secret
            user.save()
            otp = pyotp.TOTP(otp_secret, interval=1600)
            generated_otp = otp.now()
            sms_api_router(
                user.phone_number,
                f"Your Adinas Car Rent App verification OTP is {generated_otp}",
            )
            return Response(
                {"phone_number": phone_number, "message": "OTP Sent successfully"},
                status=status.HTTP_200_OK,
            )
        except UserAccount.DoesNotExist:
            return Response(
                {"message": "User  not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserLoginVerifyView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp_input = request.data.get("otp")
        try:
            user = UserAccount.objects.get(phone_number=phone_number)
            otp_secret = user.otp_secret
            otp = pyotp.TOTP(otp_secret, interval=1600)
            if otp.verify(otp_input):
                token = JWTAuthentication.create_jwt(user)
                return Response(
                    {
                        "token": token,
                        "id": user.id,
                        "phone_number": user.phone_number,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "is_owner": user.is_owner,
                        "is_driver": user.is_driver,
                        "is_both": user.is_both,
                        "message": "Logged in Successfully",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
                )
        except UserAccount.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        print(user)
        serializer = UserSerializer(user)
        return Response(
            {"message": "User Found ", "user": serializer.data},
            status=status.HTTP_200_OK,
        )


class UserViewAllAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        users = UserAccount.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserGetAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        owner = get_object_or_404(UserAccount, pk=pk)
        serializer = UserSerializer(owner)
        return Response(serializer.data)


class AssignVehicleFromSMS(APIView):
    # permission_classes =[IsAuthenticatedOrReadOnly]
    def get(self, request, vehicle_request_id, plate_id):
        vehicle_booking = get_object_or_404(VehicleBooking, id=vehicle_request_id)
        vehicle = get_object_or_404(VehicleData, plate_number=plate_id)
        assigned_vehicle = AssignedVehicle.objects.filter(
            vehicle_request=vehicle_booking, is_active=True
        )
        print(len(assigned_vehicle))
        print(vehicle_booking.no_of_vehicles)
        if len(assigned_vehicle) == vehicle_booking.no_of_vehicles:
            return Response(
                {
                    "message": "All Vehicle Requests are fulfilled  Successfully. Sorry for inconvenience."
                },
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        AssignedVehicle.objects.create(
            vehicle_request=vehicle_booking, vehicle=vehicle, is_active=True
        )
        vehicle.is_available = False
        vehicle.save()
        return Response(
            {"message": "Vehicle Assigned Successfully"}, status=status.HTTP_200_OK
        )
