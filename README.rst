=====================
django-smart-load-tag
=====================

An attempt to bring namespaces and more control to Django's ``{% load %}`` tag.

This project includes two tags: ``{% import %}`` and a replacement for the built-in ``{% load %}``. Both provide a similar feature set. The primary difference is that ``{% import %}`` namespaces by default, where ``{% load %}`` does not, retaining backwards compatibility with Django's built-in ``{% load %}`` tag.

installation
============

To install, first install the package to your system using either of the following::

    pip install django-smart-load-tag
    easy_install django-smart-load-tag

Then you must install into your Django project by adding "smart_load_tag" to your settings.INSTALLED_APPS.

If you want to use django-smart-load-tag without loading it into every template, you can install it globally by adding it to your builtin tags. Just add the following to your urlconf (usually urls.py)::

    from django.template import add_to_builtins
    add_to_builtins('smart_load_tag.templatetags.smart_load')

introduction
============

After loading, the smart ``{% load %}`` tag replaces the existing load tag, as it is backwards-compatible. It provides features that the existing load tag lacks:

templatetag namespaces:
-----------------------

::

    {% load my_tags into cool_tags %}    # Load library ``my_tags`` into namespace ``cool_tags``.
    {% cool_tags.my_tag %}               # Usage of tag ``my_tag`` imported above as part of the template library ``my_tags``.

load only a single tag from a library:
--------------------------------------

::

    {% load lib.tag_name %}    # Load tag ``tag_name`` from templatetag library ``lib``.
    {% tag_name %}             # Usage of tag imported above.

load library from a specific application:
-----------------------------------------

::

    {% load lib from my_app %}    # Ensure that library is loaded from my_app (by default, this will load the last library of that name in all your INSTALLED_APPS).

load tag as different name
--------------------------

::

    {% load my_tags.foo_tag as my_foo_tag %}    # Load tag ``foo_tag`` from library ``my_tags`` and assign to name ``my_foo_tag``
    {% my_foo_tag %}                            # Usage of tag imported above.

Thus, the syntax for the tag is described by this psuedo-regex:

::

    {% load (lib_name(.tag_name)?( from app)?( as name)?( into namespace)?,? )+ %}

examples
========

Any combination of ``from``, ``as``, and ``into`` clauses are acceptable:

::

    {% load foo_tags.my_tag from my_app into cool_tags as my_cool_tag %}    # lib foo_tags, tag my_tag, app my_app, namespace cool_tags, name my_cool_tag
    {% cool_tags.my_cool_tag %}                                             # Usage

Note that the combination of ``into`` and ``as`` are not needed, as the following two lines are equivalent:

::

    {% load foo_tags.my_tag into cool_tags as my_cool_tag %}
    {% load foo_tags.my_tag as cool_tags.my_cool_tag %}

Multiple loads can be on the same line, optionally comma separated, enabling more complex combinations such as this:

::

    {% load foo_tags from app1 into app1_foo_tags, foo_tags from app2, bar_tags.render_content as render_bar_content %}
    {% app1_foo_tags.render_content %}    # from ``foo_tags from app1 into app1_foo_tags``
    {% render_content %}                  # from ``foo_tags from app2``
    {% render_bar_content %}              # from ``bar_tags.render_content as render_bar_content``

The functionality provided by django-smart-load-tag is a progressive enhancement, and can be safely loaded into any template, as it remains backwards-compatible with Django's built-in ``{% load %}`` tag.

alternative syntax
==================

The ``{% load %}`` replacement is intended to be backwards compatible, but a new tag also exists, ``{% import %}`` that provides a syntax that defaults to providing a namespace, while allowing you to opt-out of namespacing the loaded tags (using ``* from``).

The following table illustrates the differences in syntax from the smart ``{% load %}`` tag.

    ============================================  =================================================
    {% import %} syntax                           {% load %} syntax
    ============================================  =================================================
    {% import foo_tags %}                         {% load foo_tags into foo_tags %}
    {% import foo_tags from app1 %}               {% load foo_tags from app1 into foo_tags %}
    {% import foo_tags.my_tag %}                  {% load foo_tags.my_tag as foo_tags.my_tag %}
    {% import foo_tags from my_app as my_foo %}   {% load foo_tags from my_app into my_foo %}
    {% import foo_tags.my_tag as my_foo_tag %}    {% load foo_tags.my_tag as my_foo_tag %}
    {% import * from foo_tags %}                  {% load foo_tags %}
    {% import * from foo_tags from app1 %}        {% load foo_tags from app1 %}
    ============================================  =================================================
