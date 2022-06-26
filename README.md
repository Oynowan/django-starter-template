# django-starter-template

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