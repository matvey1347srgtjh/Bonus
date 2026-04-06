from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="Транслит ссылки(URL)")

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name="Категория"
        verbose_name_plural="Категории"
        
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name="Категория")
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.PositiveIntegerField(verbose_name="Цена")
    image = models.ImageField(upload_to='merch_images/', blank=True, verbose_name="Изображение")
    stock = models.PositiveIntegerField(default=0, verbose_name="Количество")
    is_active = models.BooleanField("Активен", default=True)
    
    class Meta:
        verbose_name="Товар"
        verbose_name_plural="Товары"

    def __str__(self):
        return f"{self.name} - {self.price} Баллов"