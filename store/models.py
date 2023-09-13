from phonenumber_field.modelfields import PhoneNumberField

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class BaseModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    slug = models.SlugField(
        max_length=64,
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы '
            'латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(BaseModel):
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Product(BaseModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='products'
    )
    image = models.ImageField('Фото', upload_to='products_images', blank=True)
    value = models.FloatField(verbose_name='Объем')
    price = models.FloatField(verbose_name='Цена', blank=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('created_at',)

    def __str__(self):
        return self.title


class Order(BaseModel):
    first_name = models.CharField(
        max_length=256,
        verbose_name='Имя',
        null=False
    )
    last_name = models.CharField(
        max_length=256,
        verbose_name='Фамилия',
        null=False
    )
    # number_phone = PhoneNumberField(blank=True, verbose_name='Номер телефона')
    number_phone = models.CharField(
        max_length=11,
        verbose_name='Номер телефона'
    )
    adress = models.CharField(max_length=256, verbose_name='Адресс')
    value = models.IntegerField(verbose_name='Объем')
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        verbose_name='Местоположение',
        related_name='order'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Продукт',
        related_name='order'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('created_at',)

    def __str__(self):
        return f'Заказ {self.first_name} {self.last_name}'
