# dreamers dreamers API

[![Build Status]

## Local setup

1. Install python 3 using brew:

```commandline
brew install python3
```

2. Install virtualenv for python3:

```commandline
pip3 install virtualenv
```

3. Create a virtualenv in your local:

```commandline
mkdir venvs
cd venvs
virtualenv dreamers_api
```

4. Activate the virtualenv (needs to be activated for each new terminal):

```commandline
source dreamers_api/bin/activate
```

5. Clone the project

```commandline
git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/dreamers_api
```

6. Install project dependencies:

```commandline
cd dreaers_api
pip install -r requirements.txt
```

7. Create a dreamers_api/local_settings.py file with the following content 
(In this file you can overwrite any django settings you need):

```python
import os

DEBUG = True

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ['127.0.0.1']

CORS_ORIGIN_WHITELIST = ['http://*']

AUTH_PASSWORD_VALIDATORS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'dreamersdb'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASS', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': '5432',
        'OPTIONS': {},
        'TEST': {
            'NAME': 'dreamersdb_test',
        },
    }
}

STATIC_URL = '/dj-static/'
MEDIA_URL = '/dj-media/'
PINAX_STRIPE_SEND_EMAIL_RECEIPTS = False
```

8. Apply the migrations

```commandline
python manage.py migrate
```

9. Import the product list

```commandline
python manage.py import_inventory initial_data/Inventario.csv
```

Also create a test store with products:

```commandline
python manage.py create_test_products
```

10. Create a superuser (superuser can access the django admin):

```commandline
python manage.py createsuperuser
```

And follow the instructions.

11. Collect static files (this includes static files for the admin, django rest and swagger):

```commandline
python manage.py collectstatic
```

12. Run the project:

```commandline
python manage.py runserver
```

Django app will be available in http://127.0.0.1:8000

## Nginx setup for local development

1. Install nginx with brew

```commandline
brew install nginx
```

Start nginx by running it

```commandline
nginx
```

2. Add `local.dreamers.com` to the hosts file

```commandline
sudo vim /etc/hosts
```

Add the following line and save the file:

```
127.0.0.1 local.dreamers.com
```

3. Create the file `/usr/local/etc/nginx/servers/local.dreamers.com` with the following content:

```
upstream react {
    server 127.0.0.1:3000;
}

upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name local.dreamers.com;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    client_max_body_size 20m;

    location /v1 {
        proxy_pass http://django;
    }

    location /admin {
        proxy_pass http://django;
    }

    location /swagger {
        proxy_pass http://django;
    }

    location /api-auth {
        proxy_pass http://django;
    }

    location /dj-static {    
        autoindex on;    
        alias /Users/hugo/Projects/dreamers_api/static;    
    }

    location /dj-media {    
        autoindex on;    
        alias /Users/hugo/Projects/dreamers_api/media;    
    }

    location / {
        proxy_pass http://react;
    }
}
```

And update the `location /dj-static` and `location /dj-media` alias to match your local directory for those folders.

This file will tell nginx to:
- Serve React application from `local.dreamers.com`
- Serve django admin from `local.dreamers.com/admin`
- Serve django rest API from `local.dreamers.com/v1`
- Serve django swagger from `local.dreamers.com/swagger`
- Server django static and media files from `local.dreamers.com/dj-static` and `local.dreamers.com/dj-media`

This setup will allow the react application to use the cookie based session from django.

Reload nginx with this command:

```commandline
nginx -s reload
```

## Local database setup

Get the Postgres app from https://postgresapp.com/downloads.html and install it.

From the Postgres app start a new postgres server version 11.

Then get the pgAdmin from https://www.pgadmin.org/download/pgadmin-4-macos/ and download the latest .dmg file

Start PgAdmin and create a new server:
- Name: localhost
- Connection/Host: localhost
- Connection/Username: postgres
- SSL/SSL Mode: Prefer

Then create a new database named `dreamersdb` in your local server.


# Server configuration
1. Follow above configurations expect for steps:  9, 12. Make sure you disable debug mode
2. Add Azure storage configuration to your local_settings.py
```python
AZURE_ACCOUNT_NAME = '{name}'
AZURE_ACCOUNT_KEY = '{key}'
DEFAULT_FILE_STORAGE = 'backend.custom_azure.AzureMediaStorage'
STATICFILES_STORAGE = 'backend.custom_azure.AzureStaticStorage'
```
3. Add your stripe configurations to your local_settings.py
```python
PINAX_STRIPE_PUBLIC_KEY = '{public_key}'
PINAX_STRIPE_SECRET_KEY = '{secret_key}'
PINAX_STRIPE_SEND_EMAIL_RECEIPTS = False
```
4. `pip3 install uwsgi`. More on this [here](https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html)
5. The nginx configuration for the server is almost the same, just change the paths to match those on the server
6. Create a uwsgi.ini file for uwsgi configuration. Ej:
```
[uwsgi]
# -------------
# Settings:
# key = value
# Comments >> #
# -------------

# http
http = :8000

# Base application directory
# chdir = /full/path
chdir  = /home/ubuntu/dreamers_api

# WSGI module and callable
# module = [wsgi_module_name]:[application_callable_name]
module = dreamers_api.wsgi:application

# master = [master process (true of false)]
master = true

# processes = [number of processes]
processes = 4

daemonize = /tmp/dreamers_api.log
```
Make sure all paths match equivalents on the server
7. Run ` uwsgi --ini-paste uwsgi.ini` with this the django will be running
