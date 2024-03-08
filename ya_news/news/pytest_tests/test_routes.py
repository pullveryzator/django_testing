from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

page_data = (
    ('news:home', None),
    ('news:detail', None),
    ('users:login', None),
    ('users:logout', None),
    ('users:signup', None),
)


clients_status_data = (
    (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
    (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND),
)


@pytest.mark.parametrize(
    argnames='name, args',
    argvalues=page_data
)
def test_pages_availability(client, name, args, news):
    if name == 'news:detail':
        args = (news.id,)
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    argnames='parametrized_client, expected_status',
    argvalues=clients_status_data)
@pytest.mark.parametrize(
    argnames='name',
    argvalues=('news:edit', 'news:delete'),
)
def test_availability_and_redirect_for_comment_edit_and_delete(
        name, client, parametrized_client, comment, expected_status):
    assert comment
    url = reverse(name, args=(comment.id,))
    login_url = reverse('users:login')
    response = parametrized_client.get(url)
    assert response.status_code == expected_status
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
