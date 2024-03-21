from ..models import AreaOfInterest, VehicleData, VehicleType, VehicleModel, VehicleBrand, VehicleColor
from .serializers import (
    TypeSerializer,
    ModelSerializer,
    BrandSerializer,
    ColorSerializer,
    VehicleSerializer,
    UpdateVehicleSerializer,
    VehicleDataSerializer,
    VehicleImageSerializer,
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from .serializers import VehicleRegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics


class VehicleImageCreateView(generics.CreateAPIView):
    serializer_class = VehicleImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            vehicle_id = self.kwargs["id"]
            vehicle = VehicleData.objects.get(id=vehicle_id)
            serializer.save(vehicle=vehicle)

            response_data = {
                "error": False,
                "message": "Image Uploaded Successfully",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"message": str(e), "error": True},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VehicleDataListCreateView(generics.ListCreateAPIView):
    queryset = VehicleData.objects.all()
    serializer_class = VehicleDataSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        response_data = {
            "success": True,
            "message": "Vehicle Created Successfully",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = {"request": self.request}
        return super().get_serializer(*args, **kwargs)


class GetAllDropdownView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        brands = VehicleBrand.objects.all()
        colors = VehicleColor.objects.all()
        models = VehicleModel.objects.all()
        types = VehicleType.objects.all()
        brandSerializer = BrandSerializer(brands, many=True)
        colorSerializer = ColorSerializer(colors, many=True)
        typesSerializer = TypeSerializer(types, many=True)
        modelsSerialzer = ModelSerializer(models, many=True)
        interest_areas = ModelSerializer(AreaOfInterest.objects.all(), many=True)
        
        data = {
            "color": colorSerializer.data,
            "brand": brandSerializer.data,
            "type": typesSerializer.data,
            "model": modelsSerialzer.data,
            "area_of_interests":interest_areas.data
        }
        return Response(data, status=status.HTTP_200_OK)


class VehicleListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        vehicles = VehicleData.objects.filter(account=request.user)
        serializer = VehicleSerializer(vehicles, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        data = request.data.copy()
        data["account"] = user.id
        serializer = VehicleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VehicleDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return VehicleData.objects.get(pk=pk)
        except VehicleData.DoesNotExist:
            Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        vehicle = self.get_object(pk)
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        vehicle = self.get_object(pk)
        serializer = UpdateVehicleSerializer(
            vehicle, data=request.data, context={"request": request}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vehicle = self.get_object(pk)
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VehicleCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # parser_classes = [MultiPartParser]  # Using MultiPartParser for handling files

    def post(self, request):
        print(request.data)
        serializer = VehicleRegisterSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            object = serializer.save()
            object.area_of_interests.set(request.data["area_of_interests"])
            serialized_user = VehicleSerializer(object)
            return Response(
                {
                    "message": "Vehicle created successfully",
                    "vehicle": serialized_user.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            message = ""
            if "production_year" in serializer.errors:
                message = "Production Year : " + serializer.errors["production_year"][0]
            elif "plate_number" in serializer.errors:
                message = "Plate Number : " + serializer.errors["plate_number"][0]
            elif "price_per_day" in serializer.errors:
                message = "Daily Price : " + serializer.errors["price_per_day"][0]

            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
