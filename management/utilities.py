import os
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

env_path = settings.BASE_DIR / 'settings/.env'

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
            with open(env_path, "r") as f:
                data = f.read().split('\n')
                if data[0][:7] == 'ENV_VAR':
                    if data[0][8:] != env:
                        add = f"ENV_VAR={env}\n" + "\n".join(line for line in data[1:])
                    else:
                        add = "\n".join(line for line in data)
                else:
                        add = f"ENV_VAR={env}\n" + "\n".join(line for line in data)

                with open(env_path, 'w') as f2:
                    f2.write(add)
                    print(f"\t{bcolors.OKGREEN}->{bcolors.ENDC}Success")

            sleep(0.5)
            setup_dependencies(env)
    else:
        raise CommandError(f"Argument {env} is not correct.")

    print(f"{bcolors.OKGREEN}Successfuly changed env to {env}")

def setup_db():

    os.system('python3 manage.py makemigrations')
    os.system('python3 manage.py migrate')