from django.db import models


class Category(models.Model):
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='category_children',
    )
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
    category = models.ManyToManyField('Category', verbose_name='Categories')
    image = models.ImageField(upload_to='products/%y%m%d')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'{self.title} -- {self.category}'


class File(models.Model):
    FILE_VIDEO, FILE_AUDIO, FILE_PDF = 1, 2, 3
    FILE_TYPES = (
        (FILE_PDF, 'pdf'),
        (FILE_VIDEO, 'video'),
        (FILE_AUDIO, 'audio')
    )

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    title = models.CharField(max_length=99, verbose_name='Title')
    file = models.FileField(upload_to='files/%y%m%d', verbose_name='File')
    file_type = models.PositiveSmallIntegerField(choices=FILE_TYPES, verbose_name='File Type', default=2)
    created = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'

    def __str__(self):
        return f'{self.title} -- {self.product}'
