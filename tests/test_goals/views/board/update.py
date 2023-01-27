import pytest
from django.urls import reverse

from goals.models import BoardParticipant


@pytest.mark.django_db
def test_board_update(user_factory, get_auth_client, board_participant_factory):

    owner = user_factory()
    board_participant = board_participant_factory(user=owner)
    board_participant2 = board_participant_factory(
        board=board_participant.board, role=BoardParticipant.Role.writer
    )
    user3 = user_factory()

    data = {
        'title': board_participant.board.title,
        'participants': [
            {
                'user': board_participant2.user.username,
                'role': BoardParticipant.Role.reader,  # изменяем редактора на читателя
            },
            {
                'user': user3.username,
                'role': BoardParticipant.Role.writer,  # добавляем нового участника
            },
        ],
        'user': board_participant.user.username,
    }

    auth_client = get_auth_client(owner)
    url = reverse('detail_board', kwargs={'pk': board_participant.board.pk})

    response = auth_client.patch(
        path=url,
        data=data,
        content_type='application/json',
        HTTP_ACCEPT='application/json',
    )

    assert response.status_code == 200
    assert response.data['participants'][1]['role'] == BoardParticipant.Role.reader
    assert response.data['participants'][2]['role'] == BoardParticipant.Role.writer


@pytest.mark.django_db
def test_board_update_with_another_auth_user(
        user_factory,
        get_auth_client,
        board_participant_factory,
):
    user1 = user_factory()
    user2 = user_factory()
    board_participant = board_participant_factory(user=user1)

    data = {
        'title': 'test board',
    }

    auth_client = get_auth_client(user2)

    response = auth_client.put(
        f'/goals/board/{board_participant.board.id}',
        data=data,
        content_type='application/json',
    )

    assert response.status_code == 404
    assert response.data == {'detail': 'Страница не найдена.'}
