from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import (CategorySerializer, ProductSerializer, FileSerializer)
from .models import (Category, Product, File)
from accounts.utils import IsTokenValid # token_valid


class CategoriesView(APIView):
    def get(self, request):
        query = Category.objects.all()
        serializer = CategorySerializer(query, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryDetailView(APIView):
    def get(self, request, **kwargs):
        try:
            query = Category.objects.get(pk=kwargs['pk'])
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # the context that we passed to serializer is for that make the file url absolute not relative
        # (127.0.0.1:8000/media/... this is called absolute urls) and for send url for this api to client
        serializer = CategorySerializer(query, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductsView(APIView):
    def get(self, request):
        query = Product.objects.all()
        serializer = ProductSerializer(query, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated, IsTokenValid]

    def get(self, request, **kwargs):
        try:
            query = Product.objects.get(pk=kwargs['pk'])
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(query, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class FileView(APIView):
    def get(self, request, **kwargs):
        query = File.objects.filter(product=kwargs['product_id'])
        serializer = FileSerializer(query, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class FileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        try:
            query = File.objects.get(pk=kwargs['pk'], product=kwargs['product_id'])
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FileSerializer(query, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
