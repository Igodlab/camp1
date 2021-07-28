# Camp1 - wisdompets

This part follows the [linked learning example on wisdompets](https://www.linkedin.com/learning/paths/become-a-django-developer?u=57075641) first course.

### 1.1 Initial setup for wisdompets

Django can build for us a bunch of elemental files that cointain `main ()`"s and other stuff to run the app. In this Camp1 we will build a toy app called `wisdompets`. 

    $ django-admin startproject wisdompets

Moreover, we also have a web server ready in localhost, go to the right folder and run it and then go to a browser

```
$ cd ./wisdompets
$ ./manage.py runserver
.
.
.
July 27, 2021 - 06:41:49
Django version 3.2.5, using settings "wisdompets.settings'
Starting development server at http://127.0.0.1:8000/
```

## set PostgreSQL connections

Go to PostgreSQL as super admin 

```
$sudo -u postgres psql
postgres=#
create a user with username `camp1` and password `camp1-wisdompets`

    postgres=# CREATE USER camp1 WITH ENCRYPTED PASSWORD 'camp1-wisdompets';

We also have to modify Connection Parameters

    postgres=# ALTER ROLE camp1 SET client_encoding TO 'utf8';
    postgres=# ALTER ROLE camp1 SET default_transaction_isolation TO 'read committed';
    postgres=# ALTER ROLE camp1 SET timezone TO 'UTC';

We are setting the default encoding to UTF-8, which Django expects.

We are also setting the default transaction isolation scheme to “read committed”, which blocks reads from uncommitted transactions.

Then, we are setting the timezone by default, our Django projects will be set to use UTC.These are essential parameters recommended by the official Django team.

Also, we will grant all permissions to the `camp1` user
    
    postgres=# GRANT ALL PRIVILEGES ON DATABASE mydb TO camp1;
    postgres=# \q


**Integrate PostgreSQL with Django** open the `settings.py` file inour project and modify the default `'ENGINE': 'django.db.backends.sqlite3'`, for PostgreSQL settings

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.path.join(BASE_DIR, 'wisdompetsdb'),
        'USER': 'camp1',
        'PASSWORD': 'camp1-wisdompets',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

The default port is 5432


## Working on the app

We can create more files related to the app functionality (adoptions) itself by running from Django


    $ ./wisdompets/manage.py startapp adoptions

This creates a new folder called adoptions. Note that since a new part of the app has been added we now have to include it in the INSTALLED_APPS list in `settings.py` file under wisdompets/wisdompets

```python3
.
.
INSTALLED_APPS = [
    ...
    "adoptions",
]
.
.
```

### 2.2 Django architecture

   URL patterns      --->       Views          --->      Templates 
 wisdompets/urls.py       adoptions/views.py         adoptions/templates
                                  |
                                  |
                                Models
                          adoptions/models.py

Below a brief summary table that shows the Pieces of an App

| File or folder | Function |  |
|---|---|---|
| `apps.py`   | controls setting specific for this app |   |
| `models.py` | provides the data layer that allows to construct scheema and data queries |   |
| `admin.py`  | defines the administrative part of the app that allows to see/edit the app |   |
| `urls.py`   | allows URL routing for the app |   |
| `views.py`  | defines logic and control flow handling requests and defines the http responses that are returned |   |
| `tests.py`  | allows to run test to test the functionality of the app |   |
| migrations/ | folder that holds files that Django uses to migrate the database as we create/change our database scheema over time |   |

### 2.3 Field Types

- **Model** Defines the structure of Database. Is a class inheriting from `django.db.models.Model` and it defines database fields as class attributes. So we will have different **field Types** in Django, for more info go to the [Django docs](https://docs.djangoproject.com/en/3.2/ref/models/fields/)

    Now lets try something, go to ./adoptions/models.py and add some classes (e.g. `Pet`, `Vaccine`).

- **Migrations** create scripts to change the structure of the database. They are useful for adding, moving, removing data (some commands: `makemigrations`, `migrate`, `showmigrations`). **Initial Migration** is called to the first creation of data

    Lets create Initial Migrations, go to wisdompets home and run

    ```
    $ ./manage.py makemigrations
    Migrations for 'adoptions':
      adoptions/migrations/0001_initial.py
        - Create model Vaccine
        - Create model Pet
    ```
    
    you can also confirm this with `$ ./manage.py showmigrations`, if there are unchecked boxes you can run `$ ./manage.py migrate` and then check `showmigrations` again. 



