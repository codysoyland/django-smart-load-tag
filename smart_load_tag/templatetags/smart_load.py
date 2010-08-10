from django.template import Library, Node
from smart_load_tag.utils import load

register = Library()


class SmartLoadNode(Node):
    def render(self, context):
        return ''


class ImportNode(Node):
    def render(self, context):
        return ''


class LoaderTag(object):
    """
    Base class to implement import tags.

    Must define `parse_arguments` method, which returns a list of template
    libraries to load.
    """
    def __call__(self, parser, token):
        # remove commas (they are not semantically significant)
        args = token.contents.replace(',', '').split()
        args.pop(0) # remove command name ('load')

        # TODO: Raise appropriate template syntax errors when incorrect arguments are
        # passed. Currently a variety of random exceptions can occur.
        libs = self.parse_arguments(args)

        for lib in libs:
            self.load(parser, **lib)

        return self.node()

    def parse_lib_tag(self, token):
        """
        Parse "lib_name" or "app_name.lib_name"
        """
        lib = token.split('.')
        if len(lib) > 1:
            lib, tag = lib
        else:
            lib, tag = lib[0], '*'
        return (lib, tag)

    def load(self, *args, **kwargs):
        load(*args, **kwargs)


class LoadTag(LoaderTag):
    node = SmartLoadNode

    def parse_arguments(self, args):
        """
        Handles smart load tag argument parsing.

        Returns list of dictionaries keyed by:
            lib, tag, name, namespace, app
        """
        libs = []

        while True:
            try:
                token = args.pop(0)
            except IndexError:
                break

            lib, tag = self.parse_lib_tag(token)

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


class ImportTag(LoaderTag):
    node = ImportNode

    def parse_arguments(self, args):
        """
        Handles import tag argument parsing.

        Returns list of dictionaries keyed by:
            lib, tag, name, namespace, app
        """
        libs = []

        while True:
            try:
                token = args.pop(0)
            except IndexError:
                break

            if token == '*':
                assert args.pop(0) == 'from'
                lib, tag = self.parse_lib_tag(args.pop(0))
                namespace = None
            else:
                lib, tag = self.parse_lib_tag(token)
                namespace = lib

            # get app, namespace, and name
            app = name = None
            while True:
                try:
                    token = args.pop(0)
                except IndexError:
                    token = None
                if token == 'as':
                    if tag == '*':
                        namespace = args.pop(0)
                    else:
                        namespace = None
                        name = args.pop(0)
                elif token == 'from':
                    app = args.pop(0)
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


register.tag('load', LoadTag())
register.tag('import', ImportTag())
