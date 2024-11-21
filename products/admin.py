from django.contrib import admin
from .models import (Category, Product, File)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'is_enabled', 'created_at']
    search_fields = ['title',]
    list_filter = ['parent', 'is_enabled']


# we put this model admin in ProductAdmin by admin.StackedInline
class FileInlineAdmin(admin.StackedInline):
    model = File
    fields = ['title', 'file', 'file_type']
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title',]
    list_filter = ['category']
    # with this option for choosing different categories you don't have to hold Ctrl
    filter_horizontal = ['category']
    inlines = [FileInlineAdmin]
