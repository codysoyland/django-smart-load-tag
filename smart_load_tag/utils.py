from django.template import Library, TemplateSyntaxError, InvalidTemplateLibrary, get_templatetags_modules, import_library

def load(parser, lib, tag='*', name=None, namespace=None, app=None):
    """
    Determine and load tags into parser.

    If only a parser and lib are provided, it will behave just like Django's
    built-in {% load %} tag. Additional arguments provide more control over
    its behavior.

    Arguments:

    - parser        (required) Template parser to load the tag into.
    - lib           (required) Name of template library to load.
    - tag           If '*', it will load all tags from the given library. If a
                    string is provided, it will load a tag of that name.
    - name          Name to assign to the loaded tag (defaults to the name
                    registered to the template library object).
    - namespace     String to prepend to the name of the tag.
    - app           Tries to load the tag from the given app name.
    """
    try:
        lib_name = lib
        lib = Library()
        module_lib = get_library(lib_name, app)
        lib.tags.update(module_lib.tags)
        lib.filters.update(module_lib.filters)
        if tag != '*':
            lib.tags = {tag: lib.tags[tag]}
        if name:
            for tag in lib.tags.keys():
                lib.tags[name] = lib.tags[tag]
                if tag != name:
                    del lib.tags[tag]
        if namespace:
            for tag in lib.tags.keys():
                lib.tags['%s.%s' % (namespace, tag)] = lib.tags[tag]
                del lib.tags[tag]
        parser.add_library(lib)
    except InvalidTemplateLibrary, e:
        raise TemplateSyntaxError("'%s' is not a valid tag library: %s" % (lib, e))

def get_library(library_name, app_name=None):
    """
    (Forked from django.template.get_library)

    Load the template library module with the given name.

    If library is not already loaded loop over all templatetags modules to locate it.

    {% load somelib %} and {% load someotherlib %} loops twice.
    """
    #TODO: add in caching. (removed when forked from django.template.get_library).
    templatetags_modules = get_templatetags_modules()
    tried_modules = []
    best_match_lib = None
    last_found_lib = None
    app_name_parts = 0
    if app_name:
        app_name_parts = app_name.count('.')
    for module in templatetags_modules:
        taglib_module = '%s.%s' % (module, library_name)
        tried_modules.append(taglib_module)
        lib = import_library(taglib_module)
        if not lib:
            continue
        last_found_lib = lib

        if not app_name:
            continue

        module_list = module.split('.')
        module_list.pop() # remove the last part 'templetags'
        current_app = '.'.join(module_list)
        if current_app == app_name:
            break

        start = len(module_list) - app_name_parts - 1
        if start < 0:
            continue

        partial_app = '.'.join(module_list[start:])
        if partial_app == app_name:
            best_match_lib = lib

    if best_match_lib:
        last_found_lib = best_match_lib
    if not last_found_lib:
        raise InvalidTemplateLibrary("Template library %s not found, tried %s" % (library_name, ','.join(tried_modules)))

    return last_found_lib
