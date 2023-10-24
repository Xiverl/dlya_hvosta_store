from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


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


class Location(BaseModel):
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'район'
        verbose_name_plural = 'районы'

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True,
        validators=(RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ'
        ),)
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        null=True,
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='фамилия',
        blank=True
    )
    number_phone = models.CharField(
        max_length=11,
        verbose_name='Номер телефона',
        validators=(RegexValidator(
            regex=r'^[+*\w]$',
            message='Номер телефона пользователя содержит недопустимый символ'
        ),)
    )
    city = models.CharField(max_length=256, verbose_name='Город')
    street = models.CharField(max_length=256, verbose_name='Улица')
    building = models.CharField(max_length=256, verbose_name='Строение')
    entrance = models.CharField(max_length=256, verbose_name='Подъезд')
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Район',
        related_name='user'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username[:15]

    @property
    def is_info(self):
        atrs = [
            self.first_name,
            self.last_name,
            self.number_phone,
            self.city,
            self.street,
            self.building,
            self.entrance,
            self.location
        ]
        for atr in atrs:
            if atr is None:
                return False
        return True


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


class Type(BaseModel):
    title = models.CharField(max_length=256, verbose_name='Тип')
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
        verbose_name = 'тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.title


class Brand(BaseModel):
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
        verbose_name = 'производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.title


class Product(BaseModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='products'
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тип',
        related_name='products'
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        verbose_name='Производитель',
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
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='order'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='фамилия',
        blank=True
    )
    number_phone = models.CharField(
        max_length=11,
        verbose_name='Номер телефона',
        blank=True
    )
    city = models.CharField(
        max_length=256,
        verbose_name='Город',
        blank=True
    )
    street = models.CharField(
        max_length=256,
        verbose_name='Улица',
        blank=True
    )
    building = models.CharField(
        max_length=256,
        verbose_name='Строение',
        blank=True
    )
    entrance = models.CharField(
        max_length=256,
        verbose_name='Подъезд',
        blank=True
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        verbose_name='Район',
        related_name='order'
    )
    status = models.CharField(
        max_length=256,
        default='Оформлен',
        null=False,
        verbose_name='Статус заказа'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('created_at',)

    def __str__(self):
        return f'Заказ {self.first_name} {self.last_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Продукт',
        related_name='order'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
