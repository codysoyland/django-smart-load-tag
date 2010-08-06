from django.test import TestCase
from django.template import Template, Context

class TestSmartLoad(TestCase):
    def _render_string(self, data, context=None):
        context = context and Context(context) or Context()
        return Template(data).render(context)

    def test_basic(self):
        lib1 = (
            '{% load smart_load %}'
            '{% load lib1 %}'
            '{% tag1 %}'
            '{% tag2 %}'
        )
        lib2 = (
            '{% load smart_load %}'
            '{% load lib2 %}'
            '{% tag1 %}'
            '{% tag2 %}'
        )
        lib1_lib2 = (
            '{% load smart_load %}'
            '{% load lib1 lib2 %}'
            '{% tag1 %}'
            '{% tag2 %}'
        )
        lib2_lib1 = (
            '{% load smart_load %}'
            '{% load lib2 lib1 %}'
            '{% tag1 %}'
            '{% tag2 %}'
        )
        self.assertEqual(self._render_string(lib1), '<app 2 lib 1 tag 1><app 2 lib 1 tag 2>')
        self.assertEqual(self._render_string(lib2), '<app 2 lib 2 tag 1><app 2 lib 2 tag 2>')
        self.assertEqual(self._render_string(lib1_lib2), '<app 2 lib 2 tag 1><app 2 lib 2 tag 2>')
        self.assertEqual(self._render_string(lib2_lib1), '<app 2 lib 1 tag 1><app 2 lib 1 tag 2>')

    def test_namespace(self):
        lib1 = (
            '{% load smart_load %}'
            '{% load lib1 into lib1 %}'
            '{% lib1.tag1 %}'
            '{% lib1.tag2 %}'
        )
        self.assertEqual(self._render_string(lib1), '<app 2 lib 1 tag 1><app 2 lib 1 tag 2>')

    def test_naming(self):
        lib1 = (
            '{% load smart_load %}'
            '{% load lib1.tag1 as lib1tag1 %}'
            '{% lib1tag1 %}'
        )
        self.assertEqual(self._render_string(lib1), '<app 2 lib 1 tag 1>')
        lib2 = (
            '{% load smart_load %}'
            '{% load lib1.tag2 as lib1tag2 %}'
            '{% lib1tag2 %}'
        )
        self.assertEqual(self._render_string(lib2), '<app 2 lib 1 tag 2>')

    def test_app(self):
        app1 = (
            '{% load smart_load %}'
            '{% load lib1 from app1 %}'
            '{% tag1 %}'
            '{% tag2 %}'
        )
        self.assertEqual(self._render_string(app1), '<app 1 lib 1 tag 1><app 1 lib 1 tag 2>')
        app2 = (
            '{% load smart_load %}'
            '{% load lib1 from app2 %}'
            '{% tag1 %}'
            '{% tag2 %}'
        )
        self.assertEqual(self._render_string(app2), '<app 2 lib 1 tag 1><app 2 lib 1 tag 2>')

    def test_complex(self):
        template1 = (
            '{% load smart_load %}'
            '{% load lib1 from app1 into lib1, lib2 from app2 into lib2 %}'
            '{% lib1.tag1 %}'
            '{% lib1.tag2 %}'
            '{% lib2.tag1 %}'
            '{% lib2.tag2 %}'
        )
        self.assertEqual(self._render_string(template1),
            '<app 1 lib 1 tag 1>'
            '<app 1 lib 1 tag 2>'
            '<app 2 lib 2 tag 1>'
            '<app 2 lib 2 tag 2>'
        )

        template2 = (
            '{% load smart_load %}'
            '{% load lib1.tag2 from app2 into tags as mytag %}'
            '{% tags.mytag %}'
        )
        self.assertEqual(self._render_string(template2),
            '<app 2 lib 1 tag 2>'
        )

        template3 = (
            '{% load smart_load %}'
            '{% load lib1.tag1 from app2 as app2lib1tag2 into rockin_tags, lib2, lib2.tag2 from app1 as lib2tag2 %}'
            '{% rockin_tags.app2lib1tag2 %}'
            '{% lib2tag2 %}'
            '{% tag1 %}'
            '{% tag2 %}'
        )
        self.assertEqual(self._render_string(template3),
            '<app 2 lib 1 tag 1>'
            '<app 1 lib 2 tag 2>'
            '<app 2 lib 2 tag 1>'
            '<app 2 lib 2 tag 2>'
        )
