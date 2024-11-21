from django.urls import path
from . import views


urlpatterns = [
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('category-details/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('products/', views.ProductsView.as_view(), name='product'),

    # name for this url should be exactly {model name}-detail for HyperlinkedModelSerializer
    path('product-details/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    # this url pass the product id to api and api will show that product's all files
    # (/<int:product_id>/files/ it means show it files)
    path('product-details/<int:product_id>/file/', views.FileView.as_view(), name='file'),

    # and now we pass that specific file id either
    path('product-details/<int:product_id>/file/<int:pk>/', views.FileDetailView.as_view(), name='file-detail'),
]
