# JobPortal (Django)

Employers job post karte hain, Job Seekers apply karte hain.

## Run kaise kare (VS Code terminal me)

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

Phir browser me kholo: http://127.0.0.1:8000/

> Database (`db.sqlite3`) pehle se ready hai, demo data ke saath. `migrate` chalane ki zarurat nahi.

## Demo logins

| Role       | Username   | Password       |
|------------|------------|----------------|
| Employer   | employer1  | Demo@12345     |
| Job Seeker | seeker1    | Demo@12345     |
| Admin      | admin      | Admin@12345    |

Admin panel: http://127.0.0.1:8000/admin/

## Features

- Signup (Job Seeker ya Employer chuno), login, logout
- Jobs list with search (title / company / keyword + location) aur pagination
- Job details page with **Apply now** (ek job par ek hi baar apply)
- Employer: job post, edit, delete, apne postings dekhna, **applicants list** dekhna
- Seeker: "My applications" page
- Permissions: sirf employer job post kar sakta hai, sirf owner edit/delete kar sakta hai, employer apply nahi kar sakta
- Responsive design (mobile pe bhi)

## Useful commands

```bash
python manage.py test                 # 16 tests chalao
python manage.py createsuperuser      # naya admin banao
python manage.py seed_demo            # demo users + sample jobs dobara daalo
```

Fresh database chahiye? `db.sqlite3` delete karo, phir
`python manage.py migrate` aur `python manage.py seed_demo` chalao.

## Project structure

```
jobportal/   settings + main urls
accounts/    custom user (role), signup
jobs/        Job + Application models, views, urls, tests
templates/   base.html, login/signup, saare job pages
static/css/  style.css
```
