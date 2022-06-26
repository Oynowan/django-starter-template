# django-starter-template

## FIRST SETUP
- Create python environment. `python3 -m venv venv`
- Active venv. UNIX `source venv/bin/activate` | WIN `.\venv\Scripts\activate`
- Install django and django-environ `pip install django==4.0.5 django-environ==0.9.0`. 
- Create new django project from template `django-admin startproject --template https://github.com/Oynowan/django-starter-template/archive/master.zip {new_django_project_name} .`
- Run `python manage.py firstsetup` command
- `pytest` first test for any errors
- `python manage.py runserver` to check if everything is setup correctly (default address is `127.0.0.1:8000`)
- Congratulations your base project is ready

## COMMANDS

Main command is `python manage.py {argument}`. 

### Arguments
- `firstsetup` - Use it only once as a first command!! 
    - It installs all basic dependencies
    - It creates .env file and generates `SECRET_KEY`
    - Makes first local database migrations

- `changenv` - with option `-e prod/dev`
    - It changes environment to dev or prod
    - Installs and uninstalls dependencies 

- `whatenv` - tells on which environment you are now
- `newapp` - with `appname` as argument
    - Creates new django app in apps directory
    - Creates `apps/{appname}/tests` directory with files
        - test_models.py
        - test_views.py
        - test_urls.py
    - Adds {appname} to `INSTALLED_APPS` in django settings
    - Includes {appname} urls in main projects `urls.py`

## TESTS
For testing we are using pytest. 
- `.coveragerc` - what files to omit for coverage.
- `pytest.ini` - choose python files to test(default `test_*.py`), in `addopts` you can add any directories to check for coverage