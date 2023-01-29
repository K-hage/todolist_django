import random
import string

from django.db import models


CODE_VOCABULARY = string.digits + string.ascii_letters


class TgUser(models.Model):
    tg_id = models.BigIntegerField(
        verbose_name='telegram id',
        unique=True
    )
    tg_chat_id = models.BigIntegerField(
        verbose_name='telegram-чат id'
    )
    username = models.CharField(
        max_length=512,
        verbose_name='имя пользователя telegram',
        null=True,
        blank=True,
        default=None
    )
    user = models.ForeignKey(
        'core.User',
        models.PROTECT,
        null=True,
        blank=True,
        default=None,
        verbose_name='связанный пользователь',
    )
    verification_code = models.CharField(
        max_length=32,
        verbose_name='код подтверждения'
    )

    class Meta:
        verbose_name = 'telegram пользователь'
        verbose_name_plural = 'telegram пользователи'

    def __str__(self):
        return self.username

    def set_verification_code(self) -> None:
        self.verification_code = ''.join(random.choice(CODE_VOCABULARY) for _ in range(12))
