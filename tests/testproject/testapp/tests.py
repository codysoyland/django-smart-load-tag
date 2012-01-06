from django.test import TestCase
from django.template import Template, Context

class LoaderTestCase(TestCase):
    def render_string(self, data, context=None):
        context = context and Context(context) or Context()
        return Template(data).render(context)

    def assertTemplateRenders(self, template, output):
        self.assertEqual(self.render_string(template), output)

class SmartLoadTestCase(LoaderTestCase):
    def test_basic(self):
        """
        Standard {% load %} backwards compatibility
        """
        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% load lib1 %}'
            '{% tag1 %}'
            '{% tag2 %}'
        ,
            '<app 2 lib 1 tag 1>'
            '<app 2 lib 1 tag 2>'
        )

        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% load lib2 %}'
            '{% tag1 %}'
            '{% tag2 %}'
        ,
            '<app 2 lib 2 tag 1>'
            '<app 2 lib 2 tag 2>'
        )

        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% load lib1 lib2 %}'
            '{% tag1 %}'
            '{% tag2 %}'
        ,
            '<app 2 lib 2 tag 1>'
            '<app 2 lib 2 tag 2>'
        )

        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% load lib2 lib1 %}'
            '{% tag1 %}'
            '{% tag2 %}'
        ,
            '<app 2 lib 1 tag 1>'
            '<app 2 lib 1 tag 2>'
        )

    def test_namespace(self):
        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% load lib1 into lib1 %}'
            '{% lib1.tag1 %}'
            '{% lib1.tag2 %}'
        ,
            '<app 2 lib 1 tag 1>'
            '<app 2 lib 1 tag 2>'
        )

    def test_naming(self):
        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% load lib1.tag1 as lib1tag1 %}'
            '{% lib1tag1 %}'
        ,
            '<app 2 lib 1 tag 1>'
        )

        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% load lib1.tag2 as lib1tag2 %}'
            '{% lib1tag2 %}'
        ,
            '<app 2 lib 1 tag 2>'
        )

    def test_app(self):
        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% load lib1 from app1 %}'
            '{% tag1 %}'
            '{% tag2 %}'
        ,
            '<app 1 lib 1 tag 1>'
            '<app 1 lib 1 tag 2>'
        )

        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% load lib1 from app2 %}'
            '{% tag1 %}'
            '{% tag2 %}'
        ,
            '<app 2 lib 1 tag 1>'
            '<app 2 lib 1 tag 2>'
        )

    def test_complex(self):
        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% load lib1 from app1 into lib1, lib2 from app2 into lib2 %}'
            '{% lib1.tag1 %}'
            '{% lib1.tag2 %}'
            '{% lib2.tag1 %}'
            '{% lib2.tag2 %}'
        ,
            '<app 1 lib 1 tag 1>'
            '<app 1 lib 1 tag 2>'
            '<app 2 lib 2 tag 1>'
            '<app 2 lib 2 tag 2>'
        )

        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% load lib1.tag2 from app1 into tags as mytag1 %}'
            '{% load lib1.tag2 from app2 into tags as mytag2 %}'
            '{% tags.mytag1 %}'
            '{% tags.mytag2 %}'
        ,
            '<app 1 lib 1 tag 2>'
            '<app 2 lib 1 tag 2>'
        )

        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% load lib1.tag1 from app2 as app2lib1tag1 into rockin_tags, lib2, lib2.tag2 from app1 as lib2tag2 %}'
            '{% rockin_tags.app2lib1tag1 %}'
            '{% lib2tag2 %}'
            '{% tag1 %}'
            '{% tag2 %}'
        ,
            '<app 2 lib 1 tag 1>'
            '<app 1 lib 2 tag 2>'
            '<app 2 lib 2 tag 1>'
            '<app 2 lib 2 tag 2>'
        )

    def test_sub_app(self):
        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% load lib3 %}'
            '{% tag3 %}'
        ,
            '<app 3 sub_app1 lib 3 tag 3>'
        )

        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% load lib3 from app1 %}'
            '{% tag3 %}'
        ,
            '<app 1 lib 3 tag 3>'
        )

        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% load lib3 from sub_app1 %}'
            '{% tag3 %}'
        ,
            '<app 3 sub_app1 lib 3 tag 3>'
        )

        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% load lib3 from app3.sub_app1 %}'
            '{% tag3 %}'
        ,
            '<app 3 sub_app1 lib 3 tag 3>'
        )

class ImportTestCase(LoaderTestCase):
    def test_basic(self):
        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% import lib1 %}'
            '{% lib1.tag1 %}'
            '{% lib1.tag2 %}'
        ,
            '<app 2 lib 1 tag 1>'
            '<app 2 lib 1 tag 2>'
        )

    def test_namespace(self):
        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% import lib1 as my_lib %}'
            '{% my_lib.tag1 %}'
        ,
            '<app 2 lib 1 tag 1>'
        )

    def test_single_import(self):
        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% import lib1.tag1 %}'
            '{% lib1.tag1 %}'
        ,
            '<app 2 lib 1 tag 1>'
        )

    def test_specific_app(self):
        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% import lib1 from app1 %}'
            '{% import lib2 from app2 %}'
            '{% lib1.tag1 %}'
            '{% lib2.tag1 %}'
        ,
            '<app 1 lib 1 tag 1>'
            '<app 2 lib 2 tag 1>'
        )

    def test_specific_app_and_name(self):
        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% import lib1 from app1 as my_lib1 %}'
            '{% my_lib1.tag1 %}'
        ,
            '<app 1 lib 1 tag 1>'
        )

    def test_changed_name(self):
        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% import lib1.tag1 as my_tag %}'
            '{% my_tag %}'
        ,
            '<app 2 lib 1 tag 1>'
        )

    def test_no_namespace(self):
        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% import * from lib1 %}'
            '{% tag1 %}'
        ,
            '<app 2 lib 1 tag 1>'
        )

    def test_no_namespace_with_specific_app(self):
        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% import * from lib1 from app1 %}'
            '{% tag1 %}'
        ,
            '<app 1 lib 1 tag 1>'
        )

    def test_sub_app(self):
        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% import * from lib3 %}'
            '{% tag3 %}'
        ,
            '<app 3 sub_app1 lib 3 tag 3>'
        )

        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% import * from lib3 from app1 %}'
            '{% tag3 %}'
        ,
            '<app 1 lib 3 tag 3>'
        )

        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% import * from lib3 from sub_app1 %}'
            '{% tag3 %}'
        ,
            '<app 3 sub_app1 lib 3 tag 3>'
        )

        self.assertTemplateRenders(
            '{% load smart_load %}'
            '{% import * from lib3 from app3.sub_app1 %}'
            '{% tag3 %}'
        ,
            '<app 3 sub_app1 lib 3 tag 3>'
        )
