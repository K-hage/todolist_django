import factory
from django.contrib.auth import get_user_model
from django.utils import timezone

from goals.models import (
    Board,
    BoardParticipant,
    Goal,
    GoalCategory,
    GoalComment
)


USER_MODEL = get_user_model()


class DatesFactoryMixin(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    created = factory.LazyFunction(timezone.now)
    updated = factory.LazyFunction(timezone.now)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = USER_MODEL

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')


class BoardFactory(DatesFactoryMixin):
    class Meta:
        model = Board

    title = factory.Faker('text')


class BoardParticipantFactory(DatesFactoryMixin):
    class Meta:
        model = BoardParticipant

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)


class GoalCategoryFactory(DatesFactoryMixin):
    class Meta:
        model = GoalCategory

    board = factory.SubFactory(BoardFactory)
    title = factory.Faker('sentence', nb_words=5)
    user = factory.SubFactory(UserFactory)


class GoalFactory(DatesFactoryMixin):
    class Meta:
        model = Goal

    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(GoalCategoryFactory)
    title = factory.Faker('sentence', nb_words=5)


class GoalCommentFactory(DatesFactoryMixin):
    class Meta:
        model = GoalComment

    user = factory.SubFactory(UserFactory)
    goal = factory.SubFactory(GoalFactory)
    text = factory.Faker('text')
