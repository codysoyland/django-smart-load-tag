from django.template import Library, TextNode

register = Library()

def do_tag3(parser, token):
    return TextNode('<app 1 lib 3 tag 3>')

register.tag('tag3', do_tag3)
