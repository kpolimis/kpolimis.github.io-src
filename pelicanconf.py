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

#INDEX_SAVE_AS = 'blog_index.html'

PATH = 'content'
PAGE_ORDER_BY = 'sortorder'


# Times and dates
TIMEZONE = 'US/Pacific'
DEFAULT_LANG = u'en'

SUMMARY_MAX_LENGTH = '50'


GOOGLE_ANALYTICS = 'UA-104881568-1'

# Set the article URL
#ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
#ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

# Theme and plugins
# JINJA_FILTERS = {'sidebar': filters.sidebar}
# THEME = "pelican-themes/html5-dopetrope"

CODE_DIR = 'downloads/code'
NOTEBOOK_DIR = 'downloads/notebooks'

READERS = {'html': None}
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['liquid_tags.notebook',  # for embedding notebooks
           'summary',       # auto-summarizing articles
           'feed_summary',  # use summaries for RSS, not full articles
           'latex'
           ]
# MARKUP = ('md', )

# Only use LaTeX for selected articles

LATEX = 'article'

# SUMMARY_USE_FIRST_PARAGRAPH = 'True'

TWITTER_USERNAME = 'kpolimis'
GITHUB_USERNAME = 'kpolimis'
AUTHOR_CV = "http://kivanpolimis.com/docs/Polimis_Curriculum_Vitae.pdf"
SHOW_ARCHIVES = True

IGNORE_FILES = ['.ipynb_checkpoints']

if not os.path.exists('_nb_header.html'):
    import warnings
    warnings.warn("_nb_header.html not found.  "
                  "Rerun make html to finalize build.")
else:
    EXTRA_HEADER = open('_nb_header.html').read()

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
RELATIVE_URLS = True


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
