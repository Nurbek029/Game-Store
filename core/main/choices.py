from django.db import models

class OrderStatusEnum(models.TextChoices):
    IN_PROCESSING = ('in_processing', 'в обработке')
    DENIED = ('denied', 'Отклонено')
    ACCEPTED = ('accepted', 'Принято')