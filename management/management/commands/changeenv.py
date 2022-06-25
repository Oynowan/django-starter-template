from django.core.management.base import CommandError, BaseCommand
from management.utilities import setup_env
from django.conf import settings
import os

class Command(BaseCommand):

    warnings = 0

    warn_text = 'warning'
    help = "changeenv - changes env, by default to dev, prod or dev"
    env_path = settings.BASE_DIR / 'settings/.env'
    
    def add_arguments(self, parser) -> None:
        # optional
        parser.add_argument('env', help="Setup for environment dev or prod, default dev", default='dev')

    def handle(self, *args, **options):
        if not os.path.exists(self.env_path):
                raise CommandError('Env file doesnt exist yet, run: app firstsetup, before changing env!')
        setup_env(options['env'], True)