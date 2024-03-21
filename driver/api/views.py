from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated , IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Owner ,Driver
from .serializers import OwnerSerializer , DriverSerializer
from accounts.models import UserAccount
from django.shortcuts import get_object_or_404
from django.db import transaction

class OwnerListCreateAPIView(APIView):

    def get(self, request, *args, **kwargs):
        owners = Owner.objects.all()
        serializer = OwnerSerializer(owners, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = OwnerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    owner_instance = serializer.save()
                    return Response(
                        {"message": "Owner added successfully", "owner_id": owner_instance.id},
                        status=status.HTTP_201_CREATED
                    )
            except Exception as e:
                if 'owner_instance' in locals() and owner_instance:
                    owner_instance.delete()
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class OwnerListDetailView(APIView):
    permission_classes =[IsAuthenticatedOrReadOnly]
    def get(self, request, pk):
        owner = get_object_or_404(Owner, pk=pk)
        serializer = OwnerSerializer(owner)
        return Response(serializer.data)


    def delete(self, request, pk):
        owner = get_object_or_404(Owner, pk=pk)
        owner.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DriverListCreateAPIView(APIView):

    def get(self, request, *args, **kwargs):
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = DriverSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    driver_instance = serializer.save()
                    return Response(
                        {"message": "Driver added successfully", "driver_id": driver_instance.id},
                        status=status.HTTP_201_CREATED
                    )
            except Exception as e:
                if 'driver_instance' in locals() and driver_instance:
                    driver_instance.delete()
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DriverListDetailView(APIView):
    permission_classes =[IsAuthenticatedOrReadOnly]
    
    def get(self, request, pk):
        driver = get_object_or_404(Driver, pk=pk)
        serializer = DriverSerializer(driver)
        return Response(serializer.data)


    def delete(self, request, pk):
        driver = get_object_or_404(Driver, pk=pk)
        driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

