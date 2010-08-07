django-smart-load-tag
=====================

An attempt to bring namespaces and more control to Django's {% load %} tag.

introduction
------------

When loaded, this tag replaces the existing load tag, as it is backwards-compatible. It provides features that the existing load tag lacks:

- Templatetag namespaces:

    {% load my_tags into cool_tags %}    # Load library `my_tags` into namespace `cool_tags`.
    {% cool_tags.my_tag %}               # Usage of tag `my_tag` imported above as part of the template library `my_tags`.

- Load only a single tag from a library:

    {% load lib.tag_name %}    # Load tag `tag_name` from templatetag library `lib`.
    {% tag_name %}             # Usage of tag imported above.

- Load library from a specific application:

    {% load lib from my_app %}    # Ensure that library is loaded from my_app (by default, this will load the last library of that name in all your INSTALLED_APPS).

- Load tag as different name

    {% load my_tags.foo_tag as my_foo_tag %}    # Load tag `foo_tag` from library `my_tags` and assign to name `my_foo_tag`
    {% my_foo_tag %}                            # Usage of tag imported above.

Thus, the syntax for the tag is this psuedo-regex:

    {% load (lib_name(.tag_name)?( from app)?( as name)?( into namespace)?,? )+ %}

more examples
-------------

Any combination of `from`, `as`, and `into` clauses are acceptable:

    {% load foo_tags.my_tag from my_app into cool_tags as my_cool_tag %}    # lib foo_tags, tag my_tag, app my_app, namespace cool_tags, name my_cool_tag
    {% cool_tags.my_cool_tag %}                                             # Usage

Note that the combination of `into` and `as` are not needed, as the following two lines are equivalent:

    {% load foo_tags.my_tag into cool_tags as my_cool_tag %}
    {% load foo_tags.my_tag as cool_tags.my_cool_tag %}

Multiple loads can be on the same line, optionally comma separated, enabling more complex combinations such as this:

    {% load foo_tags from app1 into app1_foo_tags, foo_tags from app2, bar_tags.render_content as render_bar_content %}
    {% app1_foo_tags.render_content %}    # from `foo_tags from app1 into app1_foo_tags`
    {% render_content %}                  # from `foo_tags from app2`
    {% render_bar_content %}              # from `bar_tags.render_content as render_bar_content`


The functionality provided by django-smart-load-tag is a progressive enhancement, and can be safely loaded into any template, as it remains backwards-compatible with Django's built-in load tag.
