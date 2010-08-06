from django.template import Library, TextNode

register = Library()

def do_tag1(parser, token):
    return TextNode('<app 2 lib 2 tag 1>')

def do_tag2(parser, token):
    return TextNode('<app 2 lib 2 tag 2>')

register.tag('tag1', do_tag1)
register.tag('tag2', do_tag2)
