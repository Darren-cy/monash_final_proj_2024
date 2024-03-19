# Document Management System

FIT3161-62 Project, Team CS09


## Install

With python (3.12) installed, switch to the source directory and create a virtual environment:

```
py -m venv .venv
```

Then, activate the virtual environment:

```
.venv\scripts\activate
```

Install requirements:

```
py -m pip install -r requirements.txt
```

Install the latest Postgresql and run the following commands in the terminal:

```
psql

CREATE DATABASE <database_name>;

CREATE USER <username> WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE <database_name> TO <username>;

ALTER DATABASE <database_name> OWNER TO <username>;
```

Create the .env file which contains the following info:
```
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database_name>
```

And run the app:

```
flask --app dms run --debug
```

(Instructions for development only, not suitable for distribution)