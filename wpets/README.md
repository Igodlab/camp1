# Camp1 - wisdompets

This part follows the [linked learning example on wisdompets](https://www.linkedin.com/learning/paths/become-a-django-developer?u=57075641) first course.


## 1.1 set PostgreSQL connections

Go to PostgreSQL as super admin (follow the whole process [here](https://www.section.io/engineering-education/django-app-using-postgresql-database/)). Then create a database named `wisdompetsdb`


    $sudo -u postgres psql
    postgres=# CREATE DATABASE wisdompetsdb;

create a user with username `djangouser` and password `djuser`

    postgres=# CREATE USER djangouser WITH PASSWORD 'djuser';

We also have to modify Connection Parameters

    postgres=# ALTER ROLE djangouser SET client_encoding TO 'utf8';
    postgres=# ALTER ROLE djangouser SET default_transaction_isolation TO 'read committed';
    postgres=# ALTER ROLE djangouser SET timezone TO 'UTC';

We are setting the default encoding to UTF-8, which Django expects.

We are also setting the default transaction isolation scheme to “read committed”, which blocks reads from uncommitted transactions.

Then, we are setting the timezone by default, our Django projects will be set to use UTC.These are essential parameters recommended by the official Django team.

Also, we will grant all permissions to the `djangouser` user
    
    postgres=# GRANT ALL PRIVILEGES ON DATABASE wisdompetsdb TO djangouser;
    postgres=# \q

### 1.2 Initial setup for wisdompets

Django can build for us a bunch of elemental files that cointain `main ()`"s and other stuff to run the app. In this Camp1 we will build a toy app called `wisdompets`. 

```
$ django-admin startproject wisdompets
```

Moreover, we also have a web server ready in localhost, go to the right folder and run it and then go to a browser

```
$ cd ./wpets
$ ./manage.py runserver
.
.
.
July 27, 2021 - 06:41:49
Django version 3.2.5, using settings "wisdompets.settings'
Starting development server at http://127.0.0.1:8000/
```

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
        'NAME': 'wisdompetsdb',
        'USER': 'djangouser',
        'PASSWORD': 'djuser',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

The default port is 5432


## Working on the app

We can create more files related to the app functionality (adopt) itself by running from Django. Inside the project directory `/wpets/`

```
$ django-admin startapp adopt
```

This creates a new folder called adopt. Note that since a new part of the app has been added we now have to include it in the INSTALLED_APPS list in `settings.py` file under wpets/wpets

```python3
.
.
INSTALLED_APPS = [
    ...
    "adopt",
]
.
.
```

### 2.2 Django architecture

   URL patterns      --->       Views         --->      Templates 
 wisdompets/urls.py         adopt/views.py           adopt/templates
                                  |
                                  |
                                Models
                          adopt/models.py

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

To migrate to PostgreSQL as default we have to 

```
$ ./manage.py makemigrations
$ ./manage.py migrate
```

- **Model** Defines the structure of Database. Is a class inheriting from `django.db.models.Model` and it defines database fields as class attributes. So we will have different **field Types** in Django, for more info go to the [Django docs](https://docs.djangoproject.com/en/3.2/ref/models/fields/)

- Now lets try something, go to ./adopt/models.py and add some classes (e.g. `Pet`, `Vaccine`).

- **Migrations** create scripts to change the structure of the database. They are useful for adding, moving, removing data (some commands: `makemigrations`, `migrate`, `showmigrations`). **Initial Migration** is called to the first creation of data

    Lets create Initial Migrations, go to wisdompets home and run

```
$ ./manage.py makemigrations
Migrations for 'adopt':
  adopt/migrations/0001_initial.py
    - Create model Vaccine
    - Create model Pet
```
    
    you can also confirm this with `$ ./manage.py showmigrations`, if there are unchecked boxes you can run `$ ./manage.py migrate` and then check `showmigrations` again. 


### 2.4 Create csv files

Download a csv file to create data for the `adopt_pet` table in PostgreSQL in project home (same level as `manage.py`). Then make the directory `/wpets/adopt/management/commands/load_pet_data.py` and create the python script `load_pet_data.py` to read from the csv and create/update the table into PostgreSQL. Just run

```
$ ./manage.py load_pet_data
```


and check that the csv table is also now in PostgreSQL.

```
postgres=# \c wisdompetsdb
wisdompetsdb=# \dt
wisdompetsdb=# SELECT * FROM adopt_pet;
```

Great!

### 2.5 Create admin interface for the app
Lets grant admin priviliges (e.g. for the vets running the bussiness, etc.). For this inside the `/wpets/adopt/admin.py` fill

```python
from django.contrib import admin

from .models import Pet

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ["name", "species", "breed", "sex"]
```

here we are creating instances for displaying in the admin web interface. Create an admin: 

```
$ ./manage.py createsuperuser
Username (leave blank to use 'igodlab'): 
Email address: 
Password: 
Password (again):
```

where the admin user is igodlab, the email is empty, and pass: django-wpet.

### 2.6 Query data

Initialize an interactive django shell (this is different from just starting python)

```
$ python3 manage.py shell
>>> from adopt.models import Pet
>>> pets = Pet.objects.all()
>>> pets[0].name
'Pepe'
>>> petId = Pet.objects.get(id=1)
>>> petId.name
'Pepe'
```

We can also query a relational feature like vaccinations

```
>>> petId2 = Pet.objects.get(id=2)
>>> petId2.vaccinations()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
TypeError: __call__() missing 1 required keyword-only argument: 'manager'
>>> petId2.vaccinations.all()
<QuerySet []>
>>> 
```

# URL Patterns

URL pattern mathcing for handling URL requests. More info [here](https://docs.djangoproject.com/en/3.2/topics/http/urls/)

Django uses three elements inside a pattern mathcing function. They are

- First, **path converter** which is a pattern string
- Second, View to use
- Third, Name (optional) this can be used to create links to this routes


