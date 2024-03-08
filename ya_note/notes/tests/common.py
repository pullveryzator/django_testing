from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class ContentFixtureMixin(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.not_author = User.objects.create(username='Не автор')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author)
        cls.notes_list_url = reverse('notes:list')
        cls.notes_add_url = reverse('notes:add')
        cls.notes_edit_url = reverse('notes:edit', args=(cls.note.slug,))


class LogicFixtureMixin(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.form_data = {'title': 'Новый Заголовок',
                         'text': 'Новый Текст',
                         'slug': 'new_slug',
                         'author': cls.author
                         }
        cls.notes_url_add = reverse('notes:add')
        cls.url_success = reverse('notes:success')


class NoteEditDeleteMixin(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.not_author = User.objects.create(username='Не автор')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author)
        cls.form_data = {'title': 'Новый Заголовок',
                         'text': 'Новый Текст',
                         'slug': 'new_slug',
                         'author': cls.author
                         }
        cls.url_success = reverse('notes:success')
        cls.notes_edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.notes_delete_url = reverse('notes:delete', args=(cls.note.slug,))
