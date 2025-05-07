from rest_framework import serializers
from .models import Owner, Firearm

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    extra_kwargs = {
            "contact_number": {"validators": []}  # Disable unique validator
        }

class FirearmSerializer(serializers.ModelSerializer):
    # No need to explicitly declare serial_number as it's already in fields
    class Meta:
        model = Firearm
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        # No need for 'id' in fields since serial_number is now the PK

class OwnerWithFirearmsSerializer(serializers.ModelSerializer):
    firearms = FirearmSerializer(many=True, read_only=True)
    
    class Meta:
        model = Owner
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')