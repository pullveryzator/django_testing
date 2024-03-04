import pytest
from django.test.client import Client
from django.urls import reverse

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Александр Пушкин')


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Загадочный читатель')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Комментарий',
    )
    return comment


@pytest.fixture
def id_for_news(news):
    return (news.id,)


@pytest.fixture
def id_for_comment(comment):
    return (comment.id,)


@pytest.fixture
def detail_url(id_for_news):
    return reverse('news:detail', args=id_for_news)


@pytest.fixture
def delete_url(id_for_comment):
    return reverse('news:delete', args=id_for_comment)


@pytest.fixture
def edit_url(id_for_comment):
    return reverse('news:edit', args=id_for_comment)


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def comment_text():
    return 'Комментарий'


@pytest.fixture
def new_comment_text(comment_text):
    return 'Обновленный' + comment_text


@pytest.fixture
def form_data(comment_text):
    return {'text': comment_text}


@pytest.fixture
def new_form_data(new_comment_text):
    return {'text': new_comment_text}
