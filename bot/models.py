from django.db import models


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

    class Meta:
        verbose_name = 'telegram пользователь'
        verbose_name_plural = 'telegram пользователи'

    def __str__(self):
        return self.username
