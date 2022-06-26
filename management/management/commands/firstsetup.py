from django.core.management.base import CommandError, BaseCommand
from management.utilities import bcolors, setup_dependencies, setup_db, setup_env, setup_tests
from django.conf import settings
from time import sleep
import os
import datetime

class Command(BaseCommand):

    warnings = 0

    warn_text = 'warning'
    help = "firstsetup - installs dev dependencies, creates .env file with default ENV_VAR=dev, generates new SECRET_KEY, makesmigrations and migrate to db. Use it only once at the beginning, it's a one time use command."
    env_path = settings.BASE_DIR / 'settings/.env'

    def handle(self, *args, **options):
        
        start_time = datetime.datetime.now()

        # Installing base and dev equirements
        setup_dependencies(first=True)
        sleep(0.5)
        # Checking if .env already exists, if yes it writes a warning about it, if no it creates one

        print(f"\n{bcolors.OKBLUE}->{bcolors.ENDC} Creating .env file")

        if os.path.exists(self.env_path):
            warnings = setup_env(exists=True, command=False, warnings=self.warnings)
        else:
            warnings = setup_env(exists=False, command=False, warnings=self.warnings)
        sleep(0.5)
        # Setting local database, migrations

        print(f"{bcolors.OKBLUE}->{bcolors.ENDC} Setting up db")
        setup_db()
        sleep(0.5)

        # Creates pytest.ini
        print(f"{bcolors.OKBLUE}->{bcolors.ENDC} Create pytest.ini")
        setup_tests()
        sleep(0.5)
        end_time = datetime.datetime.now()
        time = end_time-start_time

        if warnings > 1:
            self.warn_text = 'warnings'

        print(f"{bcolors.OKBLUE}First setup finished in time {time.seconds}s with {warnings} {self.warn_text}. ")