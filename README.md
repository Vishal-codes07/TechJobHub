# TechJobHub – Django Job Portal

**TechJobHub** is a web-based job portal developed using Django that connects employers with job seekers. Employers can publish and manage job listings, while job seekers can explore available opportunities and apply for jobs.

## Live Demo

**Live Website:** https://techjobhub-1p1b.onrender.com

## Features

- **User Authentication:** User registration, login, and logout.
- **Role-Based Registration:** Users can register as Employers or Job Seekers.
- **Job Listings:** Browse available job opportunities with pagination.
- **Advanced Search:** Search jobs by title, company, keywords, and location.
- **Job Details:** View complete information about job postings.
- **Job Applications:** Apply for jobs with duplicate application prevention.
- **Employer Dashboard:**
  - Post new job listings.
  - Edit and delete job postings.
  - Manage personal job listings.
  - View applicants for published jobs.
- **Job Seeker Dashboard:** Track submitted applications through the My Applications section.
- **Access Control:** Only employers can post jobs, and only job owners can edit or delete their listings.
- **Responsive Design:** Optimized for desktop and mobile devices.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| Django | Backend Framework |
| HTML5 | Frontend Structure |
| CSS3 | Styling and Responsive Design |
| SQLite | Local Development Database |
| PostgreSQL | Production Database |
| Render | Cloud Deployment |
| Git & GitHub | Version Control |

## Getting Started

### Prerequisites

- Python 3
- Git
- VS Code or any code editor

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/Vishal-codes07/TechJobHub.git
cd TechJobHub
```

**2. Create a virtual environment**

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run database migrations**

```bash
python manage.py migrate
```

**5. Start the development server**

```bash
python manage.py runserver
```

Open the application:

```text
http://127.0.0.1:8000/
```

## Demo Credentials

The following credentials are available for the local demo database.

| Role | Username | Password |
|---|---|---|
| Employer | `employer1` | `Demo@12345` |
| Job Seeker | `job_seeker1` | `Demo@12345` |

> Note: Demo accounts and sample job listings belong to the local SQLite database. They are not automatically transferred to the production PostgreSQL database.

## Useful Commands

Run automated tests:

```bash
python manage.py test
```

Load demo users and sample job listings:

```bash
python manage.py seed_demo
```

Reset the local database:

Delete `db.sqlite3`, then run:

```bash
python manage.py migrate
python manage.py seed_demo
```

## Project Structure

```text
TechJobHub/
│
├── accounts/       # User authentication and role management
├── jobs/           # Job listings and application management
├── jobportal/      # Django project settings and URL configuration
├── templates/      # HTML templates
├── static/
│   └── css/        # Stylesheets
│
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

## Deployment – Render

TechJobHub is deployed on Render and uses PostgreSQL for its production database.

### Deployment Configuration

| Setting | Value |
|---|---|
| Runtime | Python 3 |
| Region | Singapore |
| Database | PostgreSQL |
| Build Command | `pip install -r requirements.txt && python manage.py collectstatic --noinput` |
| Start Command | `python manage.py migrate && gunicorn jobportal.wsgi:application` |

### Environment Variables

Configure the following environment variables in the Render Web Service:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `False` |
| `DATABASE_URL` | postgresql://techjobhub_user:g5j8O38kvoXZMimDyWrmcJuktT4suaeY@dpg-dc3v0s5g1s2s73cqtrn0-a/techjobhub|

> Security: Never commit secret keys, database credentials, or sensitive environment variables to GitHub.

## Testing

The project includes an automated test suite covering important application functionality.

Run the tests using:

```bash
python manage.py test
```

## Author

**Vishal Ahlawat**

**GitHub:** https://github.com/Vishal-codes07

**LinkedIn:** https://www.linkedin.com/in/vishal-ahlawat-0b2123257/

---

*TechJobHub – Connecting Employers with Opportunities.*
