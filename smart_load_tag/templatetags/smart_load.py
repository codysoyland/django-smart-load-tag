from django.template import Library, Node
from smart_load_tag.utils import load

register = Library()

class SmartLoadNode(Node):
    def render(self, context):
        return ''

def parse_arguments(args):
    """
    Handles smart load tag argument parsing.

    Returns list of dictionaries keyed by:
        lib, tag, name, namespace, app
    """
    libs = []

    while True:
        # parse "lib_name" or "app_name.lib_name"
        try:
            token = args.pop(0)
        except IndexError:
            break
        lib = token.split('.')
        if len(lib) > 1:
            lib, tag = lib
        else:
            lib, tag = lib[0], '*'

        # get app, namespace, and name
        app = namespace = name = None
        while True:
            try:
                token = args.pop(0)
            except IndexError:
                token = None
            if token == 'from':
                app = args.pop(0)
            elif token == 'as':
                name = args.pop(0)
            elif token == 'into':
                namespace = args.pop(0)
            elif token is None:
                break
            else:
                args.insert(0, token)
                break
        libs.append({
            'lib': lib,
            'tag': tag,
            'name': name,
            'namespace': namespace,
            'app': app,
        })

    return libs

def load_tag(parser, token):
    # remove commas (they are not semantically significant)
    args = token.contents.replace(',', '').split()
    args.pop(0) # remove command name ('load')

    libs = parse_arguments(args)

    for lib in libs:
        load(parser, **lib)

    return SmartLoadNode()

register.tag('load', load_tag)
