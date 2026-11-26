# JobPortal (Django)

Employers can post jobs, Job Seekers can apply for jobs.

## How to run (VS Code terminal)

**Mac / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

**Windows (PowerShell)**
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

After that open in Browser: http://127.0.0.1:8000/

> Database (`db.sqlite3`) is ready, no need to run. `migrate` for demo.

## Demo logins

| Role       | Username   | Password       |
|------------|------------|----------------|
| Employer   | employer1  | Demo@12345     |
| Job Seeker | seeker1    | Demo@12345     |
| Admin      | admin      | Admin@12345    |

Admin panel: http://127.0.0.1:8000/admin/

## Features

- Signup (Choose Job Seeker or Employer ), login, logout
- Jobs list with search (title / company / keyword + location) and pagination
- Job details page with **Apply now** (for one job apply once)
- Employer: job post, edit, delete, can see his/her post, **applicants list** 
- Seeker: "My applications" page
- Permissions: only employer can post jobs, only owner can edit/delete , employer can't apply for jobs
- Responsive design (mobile pe bhi)

## Useful commands

```bash
python manage.py test                 # run 16 tests 
python manage.py createsuperuser      # make a new admin
python manage.py seed_demo            # update demo users + sample jobs 
```

if u want fresh database? delete `db.sqlite3` , then run commands
`python manage.py migrate` and `python manage.py seed_demo` 

## Project structure

```
jobportal/   settings + main urls
accounts/    custom user (role), signup
jobs/        Job + Application models, views, urls, tests
templates/   base.html, login/signup, saare job pages
static/css/  style.css
```
