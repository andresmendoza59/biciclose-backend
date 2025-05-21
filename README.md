Dependencies needed:
1. External:
- PostgreSQL: 15.x.x
- PostGIS
- OSGeo4W

2. Internal (via pip):
   - asgiref==3.8.1
- Django==5.2.1
- psycopg==3.2.6
- setuptools==80.4.0
- sqlparse==0.5.3
- tzdata==2025.2

For setting up GeoDjango, follow the documentation tutorial: https://docs.djangoproject.com/en/5.2/ref/contrib/gis/install/#windows
To run this project, activate the virtual environment and run: 'py manage.py runserver'
You'd need to run these before: 'py manage.py makemigrations' && 'py manage.py migrate'
