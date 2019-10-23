from rest_framework import serializers
from .models import User, Product, Service


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = User.objects.create_superuser(**validated_data)
        return user


class StoreAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = User.objects.create_store_admin(**validated_data)
        return user


class ProductSerializer(serializers.Serializer):
    size = serializers.IntegerField()
    existence = serializers.BooleanField()
    type = serializers.IntegerField()
    price = serializers.IntegerField()

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        instance.size = validated_data.get('size', instance.size)
        instance.existence = validated_data.get('existence', instance.existence)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance

    def validate_size(self, value):
        if value < 10:
            raise serializers.ValidationError('Size of the product should me more than 10')
        return value


class ServiceSerializer(serializers.Serializer):
    approximate_duration = serializers.IntegerField()
    service_type = serializers.IntegerField()

    def create(self, validated_data):
        product = Service.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        instance.approximate_duration = validated_data.get('approximate_duration', instance.approximate_duration)
        instance.service_type = validated_data.get('service_type', instance.service_type)
        instance.save()
        return instance

    def validate_approximate_duration(self, value):
        if len(value) < 0:
            raise serializers.ValidationError('Negative duration is not allowed')
        return value
