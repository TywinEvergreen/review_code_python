from django.contrib.auth.models import User
from django.db import models


# Users - это название, которое абсолютно ни о чём нам не говорит
class AdditionalUserInformation(models.Model):
    # Несколько пробелов после оператора - это нарушение PEP8
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Юзер',
        # Без related_name нам придётся каждый раз вызывать AdditionalUserInformation.objects.get(...), неудобно
        related_name='additional_information'
    )
    # Должен быть уникальным
    inn = models.CharField(unique=True, max_length=10, verbose_name='ИНН')
    # Чтобы хранить валюту, лучше всего использовать DecimalField
    # decimal_places=2, т.к. нужна точность до копеек
    account = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = 'Дополнительная информация пользователя'
        verbose_name_plural = 'Дополнительная информация пользователей'

    def __str__(self):
        #  В python 3 использовать .format нежелатьльно, f строки гораздо удобнее для форматирования
        return f'{self.id} {self.inn}'
