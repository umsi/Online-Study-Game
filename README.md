# Online-Study-Game

## Setting up a local environment

This application uses [`virtualenv`](https://virtualenv.pypa.io/en/latest/) to manage the local development environment. Follow the steps below to set up your environment:

1. If you do not have `pip` installed, follow the instructions [here](https://pip.pypa.io/en/stable/installing/).
2. Install `virtualenv`: `pip3 install virtualenv`
3. Set up you virtual environment. From the root directory of this repository, run: `virtualenv --python=$(which python3) env`
4. Enter your new virtual environment: `source ./env/bin/activate` 
5. Install dependencies: `pip install -r requirements.txt` 
6. If running the app for the first time, build the database: `python manage.py migrate`

In development, we use `sqlite` as the database backend for convenience. In production, we use Postgres.

## Running the development server

Start Django's development server with the following command:

```
python manage.py runserver
```

You can then run the application at `localhost:8001?id=<some_id>`.

## Cleaning up

To leave your virtual environment when you've finished working on the project, run: `deactivate`.
