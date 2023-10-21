# ProjectsAutomation service

An application for assigning students to groups according to the time convenient for them.


## Setup

```bash
git clone https://github.com/nekto007/project-automation.git
cd project-automation
```
## Создать файл .env

Пример
```consbashole
SECRET_KEY=django-secret

DEBUG=True

ALLOWED_HOSTS=127.0.0.1, localhost

LANGUAGE_CODE=ru-ru
TIME_ZONE=Europe/Moscow

SENDER_EMAIL_LOGIN=example@gmail.com

SENDER_EMAIL_PASSWORD=PassWord_email

```
### 1. Install requirements

```bash
pip install -r requirements.txt
```
### 2. Run the migration to configure the SQLite database:



```bash
python3 manage.py migrate
```

### 3. Create a superuser to gain access to the admin panel:

```bash
python3 manage.py createsuperuser
```

### 4. Starts the admin panel:

```bash
python3 manage.py runserver
```

The address of the admin panel: [admin_panel](http://127.0.0.1:8000/admin/).