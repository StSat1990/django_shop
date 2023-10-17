from django.db import models

# models.py, admin.py, views.py, urls.py

class CategoryModel(models.Model):
    title = models.CharField(max_length=50)
    created_ad = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
class ProductModel(models.Model):
    title = models.CharField(max_length=50)
    category = models.ManyToManyField(CategoryModel)
    price = models.IntegerField(default=0)
    image = models.FileField(upload_to='products')
    descriptions = models.TextField(blank=True, null=True)
    product_amount = models.PositiveIntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class FormModel(models.Model):
    username = models.CharField(max_length=30, verbose_name='Имя')
    city = models.CharField(blank=True, null=True, max_length=20, verbose_name='Город')
    comment = models.TextField(verbose_name='Текст')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Форма'
        verbose_name_plural = 'Формы'

class Cart(models.Model):
    user_id = models.IntegerField()
    user_product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    user_product_quantity = models.IntegerField()
    user_add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id)