import os
import re
from time import sleep
from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.utils import get_random_secret_key

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

env_path = settings.PROJECT_PATH + '/.env'

def setup_dependencies(env='dev', first=False):
    print(f"{bcolors.OKBLUE}->{bcolors.ENDC} Installing dependencies")
    if first:
        os.system(f"pip install -r {settings.BASE_DIR/'requirements/dev.txt'}")
    else:
        if env == 'dev':
            os.system(f"pip uninstall -y -r {settings.BASE_DIR/'requirements/prod.txt'}")
            os.system(f"pip install -r {settings.BASE_DIR/'requirements/dev.txt'}")
        else:
            os.system(f"pip uninstall -y -r {settings.BASE_DIR/'requirements/dev.txt'}")
            os.system(f"pip install -r {settings.BASE_DIR/'requirements/prod.txt'}")

def check_active_env():
    if os.path.exists(env_path):
        f = open(env_path, "r")
        return f.readline()[8:].strip()
    return None

def setup_env(env="dev", exists=True, command=True, warnings=0):
    if env == 'dev' or env == 'prod':
        if not exists:
            f = open(env_path, 'w')
            f.write(f"ENV_VAR={env}\n")
            f.write(f"SECRET_KEY={get_random_secret_key()}\n")
            f.close()
            print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC} Successfuly created .env file")
        else:
            if not command:
                print(f"\t{bcolors.WARNING}->{bcolors.ENDC} File .env already exists, control your .env file if it's correct. \n\t\tIf you are not sure, delete it and run this command again. {bcolors.WARNING}{bcolors.BOLD}Don't forget to SAVE your SECRET_KEY!!!{bcolors.ENDC}")
                warnings += 1
                return warnings
            if check_active_env() == env:
                print(f"{bcolors.OKBLUE}->{bcolors.ENDC}You are already setup on {env} env")
                return
            print(f"{bcolors.OKBLUE}->{bcolors.ENDC}Changing .env file for {env}")
            reg_env = re.compile('ENV_VAR=.+')
            env_string = f"ENV_VAR={env}',\n"
            with open(env_path, "r") as f:
                data = f.read()
            check_reg = reg_env.findall(data)

            if check_reg:
                final_app_added_str = re.sub(reg_env, env_string, data)
            else:
                final_app_added_str = data + env_string

            with open(env_path, 'w') as f:
                f.write(final_app_added_str)
            print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC}Success")

            sleep(0.5)
            setup_dependencies(env)
    else:
        raise CommandError(f"Argument {env} is not correct.")

    print(f"{bcolors.OKGREEN}Successfuly changed env to {env}")

def setup_db():

    os.system('python3 manage.py makemigrations')
    os.system('python3 manage.py migrate')

def setup_tests():
    
    with open(settings.PROJECT_PATH+'/pytest.ini', 'w') as f:
        f.write(f'[pytest]\nDJANGO_SETTINGS_MODULE = {{project_name}}.config.settings\n\npython_files = test_*.py\n\naddopts = --cov=apps --cov-config=.coveragerc')