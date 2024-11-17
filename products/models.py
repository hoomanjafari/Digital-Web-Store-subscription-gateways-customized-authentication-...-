from django.db import models


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=66, verbose_name='Title')
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    avatar = models.ImageField(upload_to='categories/%y/%m/%d', verbose_name='Avatar', blank=True, null=True)
    is_enabled = models.BooleanField(default=True, verbose_name='Enabled')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return f'{self.title}'


class Product(models.Model):
    title = models.CharField(max_length=99, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%y%m%d')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'{self.title} -- {self.category}'


class File(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    title = models.CharField(max_length=99, verbose_name='Title')
    file = models.FileField(upload_to='files/%y%m%d', verbose_name='File')
    created = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'

    def __str__(self):
        return f'{self.title} -- {self.product}'
