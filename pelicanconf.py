#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os
#from utils import filters

AUTHOR = u'Kivan Polimis'
SITENAME = u'Kivan Polimis'
# SITESUBTITLE = u'my personal musings and attempts to apply \
# and share some programming tips'
SITEURL = ''

PATH = 'content'
PAGE_ORDER_BY = 'sortorder'

# Times and dates
TIMEZONE = 'US/Pacific'
DEFAULT_LANG = u'en'

# Set the article URL
#ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
#ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

# Theme and plugins
#JINJA_FILTERS = {'sidebar': filters.sidebar}
#THEME = "pelican-themes/html5-dopetrope"

CODE_DIR = 'downloads/code'
NOTEBOOK_DIR = 'downloads/notebooks'

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['summary', 'liquid_tags.img', 'liquid_tags.video',
           'liquid_tags.include_code', 'liquid_tags.notebook',
           'liquid_tags.literal', 'rmd_reader']

#{% if EXTRA_HEADER %}
#{{ EXTRA_HEADER }}
#{% endif %}


#if not os.path.exists('_nb_header.html'):
#    import warnings
#    warnings.warn("_nb_header.html not found.  "
#                  "Rerun make html to finalize build.")
#else:
#    EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8')

# RMD_READER_KNITR_OPTS_CHUNK = {'fig.path': '../../../figure/'}


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Title menu options
#MENUITEMS = [('Archives', '/archives.html'),
#             ('Home Page', 'http://<homepage>)]
#NEWEST_FIRST_ARCHIVES = False

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


#ARCHIVES_URL = "blog"
#ARCHIVES_SAVE_AS = "blog/index.html"

#PAGE_DIR = 'pages'
#PAGE_URL = '{slug}'
#PAGE_SAVE_AS = '{slug}/index.html'

#CATEGORY_URL = "category/{slug}/"
#CATEGORY_SAVE_AS = "category/{slug}/index.html"

#TAG_URL = "tag/{slug}/"
#TAG_SAVE_AS = "tag/{slug}/index.html"

#STATIC_PATHS = ['images',
#                'fonts',
#                'css',
#                'js',
#                ]
