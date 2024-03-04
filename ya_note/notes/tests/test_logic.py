from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class TestNoteCreation(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.form_data = {'title': 'Новый Заголовок',
                         'text': 'Новый Текст',
                         'slug': 'new_slug',
                         'author': cls.author
                         }
        cls.url_add = reverse('notes:add')

    def test_user_can_create_note(self):
        self.client.force_login(self.author)
        response = self.client.post(self.url_add, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.form_data['author'])

    def test_anonymous_user_cant_create_note(self):
        response = self.client.post(self.url_add, data=self.form_data)
        login_url = reverse('users:login')
        expected_url = f'{login_url}?next={self.url_add}'
        self.assertRedirects(response, expected_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)


class TestSlug(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.form_data = {'title': 'Новый Заголовок',
                         'text': 'Новый Текст',
                         'slug': 'new_slug',
                         'author': cls.author
                         }
        cls.url_add = reverse('notes:add')

    def test_not_unique_slug(self):
        self.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=self.author)
        self.client.force_login(self.author)
        self.form_data['slug'] = self.note.slug
        response = self.client.post(self.url_add, data=self.form_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=(self.note.slug + WARNING))
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_empty_slug(self):
        self.client.force_login(self.author)
        self.form_data.pop('slug')
        response = self.client.post(self.url_add, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)


class TestNoteEditDelete(TestCase):
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

    def test_author_can_edit_note(self):
        self.client.force_login(self.author)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.post(url, self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.form_data['title'])
        self.assertEqual(self.note.text, self.form_data['text'])
        self.assertEqual(self.note.slug, self.form_data['slug'])

    def test_other_user_cant_edit_note(self):
        self.client.force_login(self.not_author)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.post(url, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.pk)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)

    def test_author_can_delete_note(self):
        self.client.force_login(self.author)
        url = reverse('notes:delete', args=(self.note.slug,))
        response = self.client.post(url)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 0)

    def test_other_user_cant_delete_note(self):
        self.client.force_login(self.not_author)
        url = reverse('notes:delete', args=(self.note.slug,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 1)
