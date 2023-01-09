from rest_framework import serializers

from core.serializers import ProfileSerializer
from goals.models import (
    BoardParticipant,
    GoalCategory
)


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate_board(self, value):
        if value.is_deleted:
            raise serializers.ValidationError('нет доступа к удаленным данным')
        allow = BoardParticipant.objects.filter(
            board=value,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user=self.context['request'].user,
        ).exists()
        if not allow:
            raise serializers.ValidationError('Создавать могут только владелец и редакторы')
        return value


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')
