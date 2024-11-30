from rest_framework import serializers
from .models import (Category, Product, File)


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'avatar', 'is_enabled', 'id']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    category_children = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['title', 'description', 'avatar', 'is_enabled', 'created_at', 'id', 'url', 'category_children']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    # it's for send all the information about that category that will send to client
    # if we don't write it in this way it will just show categories their ids
    category = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ['title', 'description', 'image', 'created_at', 'id', 'url', 'category']


class FileSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    # edit somthing in file type
    file_type = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['title', 'created', 'file_type', 'id', 'product']

    # to show file type text instead of 1 2 3
    def get_file_type(self, obj):
        return obj.get_file_type_display()
