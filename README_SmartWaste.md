## Manual Build 

> 👉 STEP 1: Download the code  

```bash
$ git clone https://github.com/grecopolinga/django-material-dashboard
$ cd django-material-dashboard
```

<br />

> 👉 STEP 2: Install modules via `VENV`  

```bash
$ virtualenv env
$ source env/Scripts/activate
$ pip install -r requirements.txt
```

<br />

> 👉 STEP 3: Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> 👉 STEP 4: Create the Superuser

```bash
$ python manage.py createsuperuser
```

<br />

> 👉 STEP 5: Start the app

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`. 

<br />

NOTE: If you've previously set up and run the project, you can skip Steps 3 and 4. These steps are necessary only for the initial setup.