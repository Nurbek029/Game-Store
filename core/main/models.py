from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .choices import OrderStatusEnum

User = get_user_model()


class Category(models.Model):
    title = models.CharField(
        max_length=123,
        verbose_name='Название'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Image(models.Model):
    file = models.ImageField(
        upload_to='media/product_file',
        verbose_name='Файл'
    )

    def __str__(self):
        return str(self.file)

    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продуктов'


#  TODO: Cделать связь на таблицу User
class Game_Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=123,
        verbose_name='Название'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Категория'
    )
    main_image = models.ImageField(
        upload_to='media/main_covers',
        verbose_name='Главное фото',
        help_text='Фото которое будет отобрадажаться на обложке объявления'
    )
    images = models.ManyToManyField(
        Image,
        verbose_name='Изображения'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_product = models.ForeignKey(
        Game_Product,
        on_delete=models.CASCADE,
        verbose_name='Игра'
    )
    count = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка'
    )
    comment = models.TextField(
        max_length=500,
        verbose_name='Комментарий'
    )
    created_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.user} --> {self.game_product}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class RatingAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.ForeignKey(
        Rating,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='rating_answers'
    )
    comment = models.TextField(
        max_length=500,
        verbose_name='Комментарий'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    update_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )
    time_limit = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Ограничение по вермени'
    )

    class Meta:
        verbose_name = 'Ответ на отзыв'
        verbose_name_plural = 'Ответы на отзывы'

    def __str__(self):
        return f'{self.user} --> {self.rating}'


class PaymentMethod(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payment_methods',
        verbose_name='Пользователь'
    )
    title = models.CharField(
        max_length=123,
        verbose_name='Название'
    )
    qr_image = models.ImageField(
        upload_to='media/qr',
        verbose_name='QR'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'

    def __str__(self):
        return f"{self.user} --> {self.title}"


class PaymentRequest(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    game_product = models.ForeignKey(
        Game_Product,
        on_delete=models.CASCADE,
        verbose_name='Игра',
        related_name='orders'
    )
    is_paid = models.BooleanField(
        verbose_name='Приянто',
        default=False
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    update_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=1
    )
    check_image = models.ImageField(
        verbose_name='Чек',
        upload_to='media/check'
    )
    total_price = models.PositiveIntegerField(
        verbose_name='Сумма'
    )

    status = models.CharField(
        choices=OrderStatusEnum.choices,
        default=OrderStatusEnum.IN_PROCESSING,
        verbose_name='Статус оплаты',
        max_length=15
    )

    class Meta:
        verbose_name = 'Заявка на оплату'
        verbose_name_plural = 'Заявки на оплату'

    def __str__(self):
        return f"{self.user} --> {self.game_product}"


class Payment(models.Model):
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    user = models.CharField(
        max_length=225,
        verbose_name='Покупатель'
    )
    game_product = models.CharField(
        max_length=225,
        verbose_name='Продукт'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество'
    )
    check_image = models.ImageField(
        verbose_name='Чек',
        upload_to='media/check'
    )
    total_price = models.PositiveIntegerField(
        verbose_name='Сумма'
    ) 
    created_date = models.DateTimeField(
        auto_now_add=True,
    )
    

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
