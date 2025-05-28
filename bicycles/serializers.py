from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Bicycle, UserProfile
from django.contrib.auth.password_validation import validate_password


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'birthdate')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    profile = UserProfileSerializer(required=False)
    phone = serializers.CharField(required=False, write_only=True)
    address = serializers.CharField(required=False, write_only=True)
    birthdate = serializers.DateField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'profile', 'phone', 'address', 'birthdate')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Extraer los datos de perfil
        profile_data = {}
        if 'phone' in validated_data:
            profile_data['phone'] = validated_data.pop('phone')
        if 'address' in validated_data:
            profile_data['address'] = validated_data.pop('address')
        if 'birthdate' in validated_data:
            profile_data['birthdate'] = validated_data.pop('birthdate')
        
        # Elimina password2
        validated_data.pop('password2')
        
        # Crea el usuario
        user = User.objects.create_user(**validated_data)
        
        # Actualizar perfil si hay datos
        if profile_data:
            UserProfile.objects.filter(user=user).update(**profile_data)
            
        return user


class BicycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicycle
        fields = '__all__'
