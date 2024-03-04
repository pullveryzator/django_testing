from datetime import datetime, timedelta

import pytest
from django.utils import timezone

from news.forms import CommentForm
from news.models import Comment, News

OVER_LIMIT = 1
NEWS_COUNT_ON_HOME_PAGE = 10
COMMENT_COUNT_FOR_NEWS_PAGE = 10


def test_news_count(author_client, home_url):
    all_news = []
    for index in range(NEWS_COUNT_ON_HOME_PAGE + OVER_LIMIT):
        news = News(title=f'Новость {index}', text='Просто текст.')
        all_news.append(news)
        News.objects.bulk_create(all_news)
    response = author_client.get(home_url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, home_url):
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
    response = client.get(home_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(author, author_client, news, detail_url):
    now = timezone.now()
    for index in range(COMMENT_COUNT_FOR_NEWS_PAGE):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Комментарий № {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    response = author_client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, detail_url):
    response = author_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
