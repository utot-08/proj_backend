from rest_framework import serializers
from .models import Owner, Firearm, User

from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'role',
            'first_name',
            'last_name',
            'date_of_birth',
            'phone_number',
            'is_active',
            'date_joined'
        ]
        read_only_fields = ['is_active', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True}
        }

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'role',
            'first_name',
            'last_name',
            'date_of_birth',
            'phone_number'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True},
            'role': {'required': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'date_of_birth',
            'phone_number',
            'is_active'
        ]
class OwnerNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'  # Include whatever fields you want

class FirearmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firearm
        fields = '__all__'
        extra_kwargs = {
            'owner': {'required': False}  # This is the key change
        }
    
    def validate(self, data):
        # Remove owner if it's present in the input
        data.pop('owner', None)
        return data
# Basic serializer for simple operations
class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

# For displaying owner WITH firearms
class OwnerWithFirearmsSerializer(serializers.ModelSerializer):
    firearms = FirearmSerializer(many=True, read_only=True)
    
    class Meta:
        model = Owner
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

# Special serializer for nested creation
class OwnerCreateSerializer(serializers.ModelSerializer):
    firearms = FirearmSerializer(many=True, required=False)
    
    class Meta:
        model = Owner
        fields = '__all__'
        extra_kwargs = {
            "full_legal_name": {"validators": []},
            "contact_number": {"validators": []}
        }

    def create(self, validated_data):
        firearms_data = validated_data.pop('firearms', [])
        owner = Owner.objects.create(**validated_data)
        
        # Create firearms and automatically set the owner
        for firearm_data in firearms_data:
            Firearm.objects.create(owner=owner, **firearm_data)
            
        return owner

    def create(self, validated_data):
        firearms_data = validated_data.pop('firearms', [])
        clean_name = validated_data['full_legal_name'].strip().upper()
        
        owner, created = Owner.objects.get_or_create(
            full_legal_name__iexact=clean_name,
            defaults=validated_data
        )
        
        for firearm_data in firearms_data:
            Firearm.objects.create(owner=owner, **firearm_data)
            
        return owner
    
