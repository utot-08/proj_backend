from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Owner, Firearm
from .serializers import OwnerSerializer, FirearmSerializer, OwnerWithFirearmsSerializer

@api_view(['GET', 'POST'])
def owner_list(request):
    if request.method == 'GET':
        owners = Owner.objects.all()
        serializer = OwnerWithFirearmsSerializer(owners, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = OwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def owner_detail(request, full_legal_name):
    try:
        owner = Owner.objects.get(full_legal_name=full_legal_name)
    except Owner.DoesNotExist:
        return Response(
            {"error": f"Owner with name '{full_legal_name}' not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = OwnerWithFirearmsSerializer(owner)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = OwnerSerializer(owner, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        owner.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def firearm_list(request):
    if request.method == 'GET':
        firearms = Firearm.objects.all()
        serializer = FirearmSerializer(firearms, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = FirearmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def firearm_detail(request, serial_number):  # Changed from pk to serial_number
    try:
        firearm = Firearm.objects.get(serial_number=serial_number)  # Lookup by serial_number
    except Firearm.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = FirearmSerializer(firearm)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = FirearmSerializer(firearm, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        firearm.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def owner_firearms(request, owner_name):
    try:
        owner = Owner.objects.get(full_legal_name=owner_name)
    except Owner.DoesNotExist:
        return Response(
            {"error": f"Owner with name '{owner_name}' not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    firearms = owner.firearms.all()
    serializer = FirearmSerializer(firearms, many=True)
    return Response({
        "owner": owner.full_legal_name,
        "firearms": serializer.data
    })