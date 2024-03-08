from datetime import datetime, timedelta

import pytest
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News

OVER_LIMIT = 1
NEWS_COUNT_ON_HOME_PAGE = 10
COMMENT_COUNT_FOR_NEWS_PAGE = 10


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
def all_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Текст новости.',
            date=today - timedelta(days=index)
        )
        for index in range(NEWS_COUNT_ON_HOME_PAGE + OVER_LIMIT)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def all_comments(news, author):
    now = timezone.now()
    all_comments = [
        Comment(
            news=news,
            author=author,
            text=f'Комментарий № {index}',
            created=now + timedelta(days=index))
        for index in range(COMMENT_COUNT_FOR_NEWS_PAGE)
    ]
    Comment.objects.bulk_create(all_comments)
    return all_comments


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
