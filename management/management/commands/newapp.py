from ast import match_case
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from management.utilities import bcolors
from time import sleep
import os
import re

class Command(BaseCommand):

    help = "Creates new application in directory 'apps'. Addidtionali creates correct file structure for this project."

    def add_arguments(self, parser):
        parser.add_argument('appname', help="Name of the app")

    def handle(self, *args, **options):
        appname = options['appname']

        # CREATES NEW DJANGO APP
        print(f"{bcolors.OKBLUE}->{bcolors.ENDC} Creating new app {appname}..")
        os.system(f'mkdir apps/{appname}')
        os.system(f'python manage.py startapp {appname} apps/{appname}')
        sleep(0.5)
        # Change apps/appname/apps.py name, from appname to apps.appname
        reg_apps = re.compile(appname)

        with open(f'apps/{appname}/apps.py', 'r') as f:
            data = f.read()

        match_str = reg_apps.findall(data)[0]
        final_str = f"apps.{appname}"
        final_app_added_str = re.sub(reg_apps, final_str, data)

        with open(f'apps/{appname}/apps.py' , 'w') as f:
            f.write(final_app_added_str)

        sleep(0.5)
        
        # CREATES TEST AND URLS DIRECTORIES AND FILES
        print(f"{bcolors.OKBLUE}->{bcolors.ENDC} Creating test and urls directories/files..")

        os.system(f'mkdir apps/{appname}/tests/')

        with open(f'apps/{appname}/tests/test_models.py', 'w') as f:
            f.write('import pytest')

        with open(f'apps/{appname}/tests/test_views.py', 'w') as f:
            f.write('import pytest')

        with open(f'apps/{appname}/tests/test_urls.py', 'w') as f:
            f.write('import pytest')
        
        with open(f'apps/{appname}/urls.py', 'w') as f:
            f.write('from django.urls import path\n\nurlpatterns = [\n\n]')
        sleep(0.5)
        # ADDS APP TO SETTINGS

        print(f"{bcolors.OKBLUE}->{bcolors.ENDC} Adding {appname} to settings..")
        
        reg_apps = re.compile('\nINSTALLED_APPS = \[[^\]]*')

        with open(settings.BASE_DIR / 'settings/base.py' , 'r') as f:
            data = f.read()

        match_str = reg_apps.findall(data)[0]
        final_str = match_str + f"    'apps.{appname}',\n"
        final_app_added_str = re.sub(reg_apps, final_str, data)
        with open(settings.BASE_DIR / 'settings/base.py' , 'w') as f:
            f.write(final_app_added_str)
        sleep(0.5)
        # INCLUDES APPs URLS to main URLS

        print(f"{bcolors.OKBLUE}->{bcolors.ENDC} Including {appname} urls to main urls..")
        
        reg_urls = re.compile('\nurlpatterns = \[[^\]]*')

        with open(settings.PROJECT_PATH + '/{{project_name}}/urls.py' , 'r') as f:
            data = f.read()

        match_str = reg_urls.findall(data)[0]
        final_str = match_str + f"    # {appname}\n" + f"    path('{appname}/', include('apps.{appname}.urls')),\n"
        final_app_added_str = re.sub(reg_urls, final_str, data)
        with open(settings.PROJECT_PATH + '/{{project_name}}/urls.py' , 'w') as f:
            f.write(final_app_added_str)
        
        print(f"{bcolors.OKBLUE}->{bcolors.ENDC} You can change name of the url path in {settings.PROJECT_PATH + '/{{project_name}}/urls.py'} file.")
        sleep(1)
        print(f"{bcolors.OKGREEN} APP {appname} was addes successfuly!")