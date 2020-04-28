from django.apps import AppConfig
from shutil import copyfile
import os

from leadsapi.settings import BASE_DIR


def startup():
    print('Performing database restore..')
    DB_FILE = os.path.join(BASE_DIR, 'db.sqlite3')
    DB_RESTORE_FILE = os.path.join(BASE_DIR, 'db.sqlite3.restore')
    if os.path.exists(DB_FILE):
        copyfile(DB_FILE, DB_RESTORE_FILE)
    else:
        print('No restore changes detected!')


class MyAppConfig(AppConfig):
    name = 'restapi'
    verbose_name = "My Application"

    def ready(self):
        import os
        if os.environ.get('RUN_MAIN'):
            startup()