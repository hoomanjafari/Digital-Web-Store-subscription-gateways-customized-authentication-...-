from rest_framework import serializers
from . models import (Package, Subscription)


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    package = PackageSerializer()

    class Meta:
        model = Subscription
        fields = '__all__'
