# Document Management System

FIT3161-62 Project, Team CS09


## Setup and run backend

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

For **MacOS** users, replace the 3 above command with:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Database setup
Install the latest Postgresql and run the following commands in the terminal:

```
psql -U postgres
```

Then input the password when installing postgresql and run these commands (semicolons are important):

```
CREATE DATABASE <database_name>;
```
```
CREATE USER <username> WITH PASSWORD <password>;
```
```
GRANT ALL PRIVILEGES ON DATABASE <database_name> TO <username>;
```
```
ALTER DATABASE <database_name> OWNER TO <username>;
```

Create the .env file which contains the following info:
```
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database_name>
JWT_SECRET_KEY="YourSecretKey"
VITE_API_URL="http://127.0.0.1:5000"
VITE_BACKEND_API_URL="http://127.0.0.1:5000/api/v1.0"
VITE_TINYMCE_API_KEY="5yvunx1guc0lr4adzohtbndujkqku1ett0wj78ajur6497i3"
```

Create the .flaskenv file which contains the following info (This should aready be created, skippable):

```
FLASK_APP = dms
FLASK_ENV= development
FLASK_DEBUG = True
```

Create all the tables in the postgresql database

```
flask db init
```
```
flask db migrate
```
```
flask db upgrade
```

And run the app:

```
flask run
```

# Setup and run frontend

With [Nodejs](https://nodejs.org/en/download) installed, run the following commands:
```
cd frontend
npm install
npm run dev
```

(Instructions for development only, not suitable for distribution)

## See also

* [Internal API documentation>.](docs/api.md)