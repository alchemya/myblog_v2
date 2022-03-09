__author__ = 'yuchen'
__date__ = '2019/3/5 23:43'

import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('KKBlog Admin', MAIL_USERNAME)

    KKBLOG_EMAIL = os.getenv('KKBLOG_EMAIL')
    KKBLOG_POST_PER_PAGE = 10
    KKBLOG_MANAGE_POST_PER_PAGE = 15
    KKBLOG_COMMENT_PER_PAGE = 15
    CKEDITOR_HEIGHT = 400
    CKEDITOR_SERVE_LOCAL = True

    # ('theme name', 'display name')
    KKBLOG_THEMES = {'perfect_blue': 'Light Blue', 'perfect_red': 'Phoenix Red',
                     'perfect_darkly': 'Darkly','perfect_sketch': 'Perfect Sketch'}


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

