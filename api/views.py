from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Owner, Firearm
from .serializers import (
    OwnerSerializer, 
    FirearmSerializer, 
    OwnerWithFirearmsSerializer,
    OwnerCreateSerializer  # Add this import
)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Allow anyone to access
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        
        # Get query parameters
        search_query = request.query_params.get('search', None)
        role_query = request.query_params.get('role', None)
        
        # Apply filters if they exist
        if search_query:
            users = users.filter(username__icontains=search_query)
            # If you want to search first_name and last_name as well:
            # users = users.filter(Q(username__icontains=search_query) | 
            #                    Q(first_name__icontains=search_query) |
            #                    Q(last_name__icontains=search_query))
        
        if role_query:
            users = users.filter(role=role_query)
            
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])  # Allow anyone to access
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        
        
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def owner_list(request):
    if request.method == 'GET':
        owners = Owner.objects.all()
        serializer = OwnerWithFirearmsSerializer(owners, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Handle both simple owner creation and owner+firearms creation
        if 'firearms' in request.data:
            serializer = OwnerCreateSerializer(data=request.data)
        else:
            serializer = OwnerSerializer(data=request.data)
            
        if serializer.is_valid():
            owner = serializer.save()
            response_serializer = OwnerWithFirearmsSerializer(owner)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def owner_detail(request, full_legal_name):
    try:
        # Case-insensitive lookup
        owner = Owner.objects.get(full_legal_name__iexact=full_legal_name)
    except Owner.DoesNotExist:
        return Response(
            {"error": f"Owner with name '{full_legal_name}' not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = OwnerWithFirearmsSerializer(owner)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Use OwnerSerializer for updates (without firearms)
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
        firearms = Firearm.objects.all().select_related('owner')  # Optimize query with select_related
        serializer = FirearmSerializer(firearms, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = FirearmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def firearm_detail(request, serial_number):
    try:
        firearm = Firearm.objects.get(serial_number=serial_number)
    except Firearm.DoesNotExist:
        return Response(
            {"error": f"Firearm with serial number '{serial_number}' not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
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
        owner = Owner.objects.get(full_legal_name__iexact=owner_name)
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



@api_view(['PATCH'])

def update_firearm_status(request, serial_number):
    try:
        firearm = Firearm.objects.get(serial_number=serial_number)
    except Firearm.DoesNotExist:
        return Response(
            {"error": f"Firearm with serial number '{serial_number}' not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'PATCH':
        # Only allow updating the status field
        serializer = FirearmSerializer(firearm, data=request.data, partial=True)
        if serializer.is_valid():
            # You might want to add additional validation here
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def owner_detail_by_id(request, pk):
    try:
        owner = Owner.objects.get(pk=pk)
    except Owner.DoesNotExist:
        return Response(
            {"error": f"Owner with ID '{pk}' not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = OwnerWithFirearmsSerializer(owner)
        return Response(serializer.data)        
    

@api_view(['GET'])
def get_owner_by_id(request, pk):
    """
    Retrieve a specific owner by their primary key (ID)
    """
    try:
        owner = Owner.objects.get(pk=pk)
        serializer = OwnerWithFirearmsSerializer(owner)
        return Response(serializer.data)
    except Owner.DoesNotExist:
        return Response(
            {"error": f"Owner with ID {pk} not found"},
            status=status.HTTP_404_NOT_FOUND
        )
