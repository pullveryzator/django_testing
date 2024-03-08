from notes.forms import NoteForm

from .common import ContentFixtureMixin


class TestContent(ContentFixtureMixin):

    def test_note_in_list_for_author(self):
        self.client.force_login(self.author)
        response = self.client.get(self.notes_list_url)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_note_not_in_list_for_another_user(self):
        self.client.force_login(self.not_author)
        response = self.client.get(self.notes_list_url)
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_create_note_page_contains_form(self):
        self.client.force_login(self.author)
        response = self.client.get(self.notes_add_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_edit_note_page_contains_form(self):
        self.client.force_login(self.author)
        response = self.client.get(self.notes_edit_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
