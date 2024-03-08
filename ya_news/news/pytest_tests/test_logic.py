from http import HTTPStatus

from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

COMMENT_TEXT = 'Комментарий'
NEW_COMMENT_TEXT = 'Обновленный комментарий'
form_data = {'text': COMMENT_TEXT}
new_form_data = {'text': NEW_COMMENT_TEXT}


def test_anonymous_user_cant_create_comment(client, detail_url):
    assert Comment.objects.count() == 0
    client.post(detail_url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(
        author,
        author_client,
        news,
        detail_url):
    assert Comment.objects.count() == 0
    response = author_client.post(detail_url, data=form_data)
    assertRedirects(response, f'{detail_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, detail_url):
    assert Comment.objects.count() == 0
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(detail_url, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, detail_url, delete_url):
    assert Comment.objects.count() == 1
    url_to_comments = detail_url + '#comments'
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(
        reader_client,
        delete_url):
    assert Comment.objects.count() == 1
    response = reader_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(
        author_client,
        comment,
        detail_url,
        edit_url):
    assert Comment.objects.count() == 1
    url_to_comments = detail_url + '#comments'
    response = author_client.post(edit_url, data=new_form_data)
    assertRedirects(response, url_to_comments)
    comment = Comment.objects.get()
    assert comment.text == NEW_COMMENT_TEXT


def test_user_cant_edit_comment_of_another_user(
        reader_client,
        comment,
        edit_url):
    assert Comment.objects.count() == 1
    response = reader_client.post(edit_url, data=new_form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
