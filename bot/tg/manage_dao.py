from goals.models import (
    Goal,
    GoalCategory
)


class ManageDAO:
    def __init__(self):
        self.storage_for_create = {}
        self.response = {}

    def goals(self, tg_user):
        """
        Возвращает словарь с целями и
        сгенерированным сообщением об этих целях
        """

        goals = (
            Goal.objects.filter(category__board__participants__user=tg_user.user).
            exclude(status=Goal.Status.archived)
        )
        self.response['goals'] = goals

        if goals.count() > 0:
            goals_for_msg = [f'# {item.id} [{item.title}]' for item in goals]
            self.response['message'] = 'Ваши цели:\n' + '\n'.join(goals_for_msg)
        else:
            self.response['message'] = 'Список целей пуст'
        return self.response

    def category(self, tg_user):
        """
        Возвращает словарь с категориями и
        сгенерированным сообщением об этих категорий
        """

        category = GoalCategory.objects.filter(
            board__participants__user=tg_user.user,
            is_deleted=False
        )
        self.response['category'] = category

        if category.count() > 0:
            goals_for_msg = [f'# {item.id} [{item.title}]' for item in category]
            self.response['message'] = 'Ваши категории:\n' + '\n'.join(goals_for_msg)
        else:
            self.response['message'] = 'Список категорий пуст'
        return self.response

    def input_category(self, msg, tg_user):
        """
        Записывает в словарь выбранную категорию для создания цели
        возвращает словарь с выбранной категорией и
        сгенерированным сообщением ответа
        """

        category = GoalCategory.objects.filter(
            title__exact=msg.text,
            board__participants__user=tg_user.user,
            is_deleted=False
        ).first()

        if category:
            self.response['category'] = category
            self.storage_for_create['category'] = category
            self.response['message'] = 'Отлично!\nВведите название цели:'
        else:
            self.response['message'] = 'Такой категории нет!\nВыберите из имеющихся!\n'
            self.response['message'] += self.category(tg_user)['message']
        return self.response

    def input_title_goal(self, msg, tg_user):
        """
        Создает цель в бд
        возвращает словарь с созданной целью и
        сгенерированным сообщением ответа
        """
        category = self.storage_for_create['category']
        goal = Goal.objects.create(
            user=category.user,
            title=msg.text,
            category=category
        )

        self.response['goal'] = goal

        if goal:
            self.response['message'] = 'Цель создана'
        return self.response

    def start_creating_goal(self, tg_user):
        """
        Для начала создания цели.
        Очищает словарь создания цели,
        возвращает словарь со
        сгенерированным сообщением ответа
        """

        self.storage_for_create = {}
        self.response['message'] = 'Выберите в какой категории создать цель!\n' + self.category(tg_user)['message']
        return self.response

    def cancel(self):
        """
        Для отмены создания цели.
        Очищает словарь создания цели,
        возвращает словарь со
        сгенерированным сообщением ответа
        """

        self.storage_for_create = {}
        self.response['message'] = 'Операция отменена'
        self.response['items'] = self.storage_for_create
        return self.response
