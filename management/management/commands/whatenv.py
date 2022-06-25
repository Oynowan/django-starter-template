from django.core.management.base import BaseCommand
from management.utilities import check_active_env, bcolors
from django.conf import settings
import os

class Command(BaseCommand):

    help = "whatenv - tells which env is active"
    env_path = settings.BASE_DIR / 'settings/.env'

    def handle(self, *args, **options):
        print(f"\n\t{bcolors.OKBLUE}Active env: {check_active_env()}\n")