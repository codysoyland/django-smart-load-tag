import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.rst')

setup(
    name = "django-smart-load-tag",
    version = "0.3.2",
    url = 'http://github.com/codysoyland/django-smart-load-tag',
    license = 'BSD',
    description = "An attempt to bring namespaces and more control to Django's {% load %} tag.",
    long_description = README,
    author = 'Cody Soyland',
    author_email = 'codysoyland@gmail.com',
    packages = [
        'smart_load_tag',
        'smart_load_tag.templatetags',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
