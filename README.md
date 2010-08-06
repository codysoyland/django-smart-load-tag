Intro
=====

django-smart-load-tag is an attempt to bring namespaces and more control to Django''s {% load %} tag.

Documentation
=============

Full documentation has not yet been written. Please refer to the tests (in tests/testproject/testapp/tests.py) or the following examples for now.

Example
=======

Example app/taglib hierarchy
----------------------------

    app1
        foo_tags
            - render_content
        bar_tags
            - render_content
            - render_bar
    app2
        foo_tags
            - render_content

Old syntax
----------

    {% load <lib_name> %}

New syntax
----------

    {% load <lib_name>[.<tag_name>][ from <app>][ as <name>][ into <namespace>](, ) %}

Backwards compatible
--------------------

    {% load foo_tags bar_tags %}
        -> {% render_content %} (from app1.bar_tags)
        -> {% render_bar (from app1.bar_tags)

    {% load bar_tags foo_tags %}
        -> {% render_content %} (from app1.foo_tags)
        -> {% render_bar %} (from app1.bar_tags)

Import from specific app
------------------------

    {% load foo_tags from app2 %}
        -> {% render_content %} (from app2.foo_tags)

Import from specific library
----------------------------

    {% load bar_tags.render_content %}
        -> {% render_content %} (from app1.bar_tags)

Customize name
--------------

    {% load foo_tags.render_content as render_foo %}
        -> {% render_foo %} (from app1.foo_tags.render_content)

Load into namespace
-------------------

    {% load bar_tags into bar_tags %}
        -> {% bar_tags.render_content %} (from app1)
        -> {% bar_tags.render_bar %} (from app1)

Load specific app's library into namespace
------------------------------------------

    {% load foo_tags from app2 into app2_foo_tags %}
        -> {% app2_foo_tags.render_content %} (from app2)

Complex example
---------------

    {% load foo_tags from app1 into app1_foo_tags, foo_tags from app2, bar_tags.render_content as render_bar_content %}
        -> {% app1_foo_tags.render_content %} (app1.foo_tags.render_content)
        -> {% render_content %} (app2.foo_tags.render_content)
        -> {% render_bar_content %} (app1.bar_tags.render_content)

