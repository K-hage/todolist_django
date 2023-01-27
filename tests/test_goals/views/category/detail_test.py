import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_category_detail(get_auth_client, board_participant, category):

    auth_client = get_auth_client(board_participant.user)

    url = reverse('detail_category', kwargs={'pk': category.pk})
    response = auth_client.get(
        path=url
    )

    assert response.status_code == status.HTTP_200_OK
    assert not response.data['is_deleted']


@pytest.mark.django_db
def test_category_detail_not_auth_user(client, board_participant, category):

    url = reverse('detail_category', kwargs={'pk': category.pk})
    response = client.get(
        path=url
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {
        'detail': 'Учетные данные не были предоставлены.'
    }


@pytest.mark.django_db
def test_category_detail_not_owner(auth_client, category):

    url = reverse('detail_category', kwargs={'pk': category.pk})
    response = auth_client.get(
        path=url
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {'detail': 'Страница не найдена.'}
