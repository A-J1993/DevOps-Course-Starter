# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App (Non-Docker instructions)

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
OR if one wants to run it on a Vagrant VM

```bash
$ vagrant up
```

(There won't be a message on the output as it would be directed to a logs file)

Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

The flask app has now been altered so that it is now integrated to the MongoDB Server.

In order to run the app one needs to have access to a MongoDB Client and to ensure one has the correct Mongo Client connection string in their environment file. 

In order to test if the app is working, type into the command line 

```bash
$ poetry run pytest
```

although if one only wants to launch the end-to-end tests add in `test_e2e` at the end of the command, or `tests` if one only wants to launch unit and integration tests.

NOTE: For the End to End Tests to function, one needs to have `geckodriver.exe` in the root folder and have Mozilla Firefox installed in the Computer.

## Running the App (Docker instructions)

Assuming one has already installed Docker and tested it works to get the app running, first build the image by running:

```bash
$ docker build --target <stage> --tag <tag> .
```

Where ```<stage>``` is either ```base```, ```development```, or ```production```, and ```<tag>``` is a tag of your choosing 

If just wanting to run the image on production, run:

```bash
$ docker run --env-file .env  -p 8000:8080 <tag> 
```

If wanting to run the development or the production build (which should be done via a bind mount), enter on the command line:

```bash
$ docker run --env-file .env -p 8080:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app <tag> 
```

And then go to [`http://localhost:8080/`](http://localhost:8080/) to view the app.

(You also have the oppotunity to input the ```--detach``` tag after ```docker run``` if you want to run the conatainer in the "background")

In addition one can also run Pytests via Docker. Simply build the image from the ```test``` stage

```bash
$ docker build --target test --tag <tag> .
```

And then run the image

```bash
$ docker run <tag> tests
```

For unit and integration tests. Or

```bash
$ docker run --env-file .env <tag> test_e2e
```

for end-to-end testing

## Instrictions for CI/CD build

While one can run pull request builds at ease via the Travis Website, one can only use Continuous Delivery with a git push build (a build that occurs in Travis once there is a git push) which then deploys the application via terraform.
