# Saloon Management App

A small Django project for managing workers, appointments and payments with a TailwindCSS-powered dashboard. Intended as a dev-friendly, fast-production app using SQLite, Django w/ templating and django-tailwind for styling.
<br> Uses MVT architecture to deliver a full functional web-service.



## Quick overview

- 💻 Backend: **Django** (Python)
- 🎨 Styling: **TailwindCSS** integrated via **django-tailwind**
- 📄 DB: **SQLite** (`db.sqlite3`) (local)
- 🚀 Development status: Authorization, Data management and edition, and Payments section yet in TODO



## Features

- Management dashboards with fast overview of daily-usefull data
- Appointments list with status and schedule
- Registration of Services, Workers, Clients involved in Appointments and Payments.


## Prerequisites

- Python 3.10+ (developed in 3.13.2)
- `virtualenv` / built-in `venv`
- node.js + npm for Tailwind build. **commits are already builded, ready to run**...

    On Windows make sure `npm` path is available. If `manage.py tailwind install`\ `start` complains, set `NPM_BIN_PATH` in `settings.py` to the absolute path of `npm.cmd`, e.g.:
    ```py
    NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
    ```


---


## Local install and run

**1.** Clone the repo and enter project folder

```bash
git clone https://github.com/limatila/saloon-mgmt-app
cd saloon-mgmt-app
git status #check
```

**2.** Create & activate a virtualenv 

```bash
# (optional if you want to isolate needed environment)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

**3.** Install Python requirements

```bash
#now, with vENV activated (displays '(venv)' at start of the prompt)
pip install -r requirements.txt
```

**4.** Create a `.env` file in the `src/` folder (optional, not needed)

 Your `settings.py` will load `SECRET_KEY` from the env.
```env
SECRET_KEY=replace-with-a-long-and-strong-secret
```


**5.** Create a superuser so you can access django's "admin/"

```bash
python src/manage.py createsuperuser
# and follow the steps django will present you
```

> If you prefer, there's already a registered user you can login, using: **user**: `user`, **password**: `12345678Ab`

**6.** Start Django dev server

```bash
python ./src/manage.py runserver
```

**7.** Open the web site at:
    **[http://127.0.0.1:8000/](http://localhost:8000/)**


---


## Build tailwindcss for production
**1.** Install tailwind dependencies (initial, only once)

```bash
python manage.py tailwind install
```
> This will run `npm install` inside the Tailwind app (`src/saloon/static_src/` or the configured Tailwind **app).** If it fails, ensure node & npm are installed and `NPM_BIN_PATH` is correct.

**2.** Start Tailwind dev watcher (in a separate terminal)

```bash
# from src/
python src/manage.py tailwind start
```

**3.** Collect static files

```bash
python src/manage.py collectstatic --noinput
```

## Important paths

- `src/manage.py` — Django management and execution script
- `src/db.sqlite3` — local database file (SQLite) with intended deliver / test data
- `src/static/` — uploaded media, style, and script files

### *For tailwind build info*
- `src/saloon/static_src/` — Tailwind source (input.css, package.json, tailwind.config.js)
- `src/saloon/static/css/dist/` — Tailwind compiled output (dist)



## Troubleshooting

### You can submit your issue to the github issues tab.
- or email me at ***atilalimade@gmail.com***


## Useful commands summary

```bash
python src/manage.py makemigrations #and migrate
python src/manage.py check #check for errors and warnings
```
