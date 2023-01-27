import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_list_comment(get_auth_client, board_participant, goal, goal_comment_factory):

    goal_comment_factory.create_batch(
        5,
        user=board_participant.user,
        goal=goal
    )

    auth_client = get_auth_client(board_participant.user)

    url = reverse('list_comment')
    response = auth_client.get(
        path=url
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5


@pytest.mark.django_db
def test_list_comment_not_owner(auth_client, goal_comment_factory):
    goal_comment_factory.create_batch(5)

    url = reverse('list_comment')
    response = auth_client.get(
        path=url
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0
