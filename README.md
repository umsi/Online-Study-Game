# Online-Study-Game

This repository contains code for running the `invest_game` study and supporting questionnaires. It also contains (deprecated!) non-`invest_game` code designed to run other game experiments. This functionality is siloed in its own Django app but could be restored in the future.

## Setting up a local environment

This application uses [`virtualenv`](https://virtualenv.pypa.io/en/latest/) to manage the local development environment. Follow the steps below to set up your environment:

1. If you do not have `pip` installed, follow the instructions [here](https://pip.pypa.io/en/stable/installing/).
2. Install `virtualenv`: `pip3 install virtualenv`
3. Set up you virtual environment. From the root directory of this repository, run: 
```
virtualenv --python=$(which python3) env
```
4. Enter your new virtual environment: `source ./env/bin/activate` 
5. Install dependencies: `pip install -r requirements.txt` 
6. If running the app for the first time, build the database: `python manage.py migrate`

In development, we use `sqlite` as the database backend for convenience. In production, we use Postgres.

## Running the development server

Start Django's development server with the following command:

```
python manage.py runserver
```

You can then run the application at `localhost:8000?id=<some_id>`.

## Cleaning up

To leave your virtual environment when you've finished working on the project, run: `deactivate`.

## Deployment

The application is configured to be deployed to an Elastic Beanstalk environment in AWS. This readme assumes that the EB environment is already set up. The environment should have a Postgres database instance connected to it.

Assuming such an environment exists, the application can be deployed by running:
```
eb deploy <environment_name>
```
where `<environment_name>` is the name of the EB environment. If no `<environment_name>` is supplied, the deployment will default to an environment called `Online-Study-Game`. It's intended that the default environment name be used for the production application.

If you need to create an environment, use the `eb create` command, documented [here](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.environments.html).

## Admin panel

The standard Django admin application can be accessed at `<application_url>/admin`. The username and password are set using a database fixture found in `games/invest_game/fixtures/users.json`.

From the admin panel, you can export study data to a CSV file.

## Running tests

Run tests with:
```
python manage.py test
```
