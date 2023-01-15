from enum import (
    Enum,
    auto
)

from django.conf import settings
from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from bot.tg.manage_dao import ManageDAO


class Command(BaseCommand):
    help = 'run bot'

    class Status(Enum):
        idle = auto(), 'Бездействие'
        input_category = auto(), 'Введена категории для создания цели'
        input_title_goal = auto(), 'Введено название цели'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.TG_BOT_TOKEN)
        self.manage = ManageDAO()
        self.status = self.Status.idle

    def handle(self, *args, **kwargs):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            tg_id=msg.from_.id,
            defaults={
                'tg_chat_id': msg.chat.id,
                'username': msg.from_.username,
            },
        )

        if created:
            self.tg_client.send_message(msg.chat.id, 'Привет!')

        if tg_user.user:
            self.handle_verified_user(msg, tg_user)
        else:
            self.handle_user_without_verification(msg, tg_user)

    def handle_verified_user(self, msg: Message, tg_user: TgUser):
        if not msg.text:
            return

        if msg.text.startswith('/'):
            resp = self.check_commands(msg, tg_user)
            self.tg_client.send_message(msg.chat.id, resp.get('message'))
            return

        if self.status == self.Status.input_category:
            resp = self.manage.input_category(msg, tg_user)
            if resp.get('category'):
                self.status = self.Status.input_title_goal

        elif self.status == self.Status.input_title_goal:
            resp = self.manage.input_title_goal(msg, tg_user)
            self.status = self.Status.idle
        else:
            resp = {'message': "Чего изволите?\nПопробуйте указать команду начиная со знака '/'"}

        self.tg_client.send_message(msg.chat.id, resp.get('message'))

    def check_commands(self, msg, tg_user):
        if '/goals' == msg.text:
            resp = self.manage.goals(tg_user)

        elif '/site' == msg.text:
            resp = {'message': settings.DOMAIN_SITE}

        elif '/create' == msg.text:
            self.status = self.Status.input_category
            resp = self.manage.start_creating_goal(tg_user)

        elif '/cancel' == msg.text:
            resp = self.manage.cancel()
            if not resp.get('items'):
                self.status = self.Status.idle
        else:
            resp = {'message': 'Неизвестная команда'}
        return resp

    def handle_user_without_verification(self, msg: Message, tg_user: TgUser):
        tg_user.set_verification_code()
        tg_user.save(update_fields=['verification_code'])
        self.tg_client.send_message(
            msg.chat.id,
            f'Код подтверждения:\n{tg_user.verification_code}\n'
            f'Ссылка на сайт:\n{settings.DOMAIN_SITE}'
        )
