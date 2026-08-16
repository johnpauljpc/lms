# JPC Academy - Learning Management System

A full-featured **Django Learning Management System** built for Nigerian learners, with course enrollment, video lessons, Naira pricing and secure authentication.

## Features

- **Authentication** - register, login/logout, email-based password reset, profile with password validation
- **Course catalog** - browse/filter courses by category, level and price; search courses
- **Course pages** - detailed overview, curriculum with per-lesson video lessons, instructor bios and reviews
- **Enrollment** - free courses auto-enroll; paid courses go through a Nigerian checkout (Paystack / bank transfer / WhatsApp)
- **My Courses & Watch** - enrolled students get their own dashboard to stream lessons
- **Naira pricing** - discount calculation + `naira` template filter
- **Security** - hardened settings (env-based secret key, secure cookies, HTTPS redirects in production)

## Tech Stack

- Python / Django 6
- SQLite by default, PostgreSQL optional via `DATABASE_URL`
- Bootstrap 5 + custom theme (HTML/CSS/JS)
- Pillow (image handling)

## Screenshots

![Home](screenshots/home.png)
![Courses](screenshots/courses.png)
![Course Detail](screenshots/course-detail.png)
![About](screenshots/about.png)
![Contact](screenshots/contact.png)
![Login](screenshots/login.png)
![Register](screenshots/register.png)

## Quick Start

```bash
python -m venv env
source env/bin/activate          # Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open <http://127.0.0.1:8000>.

Create an admin account:

```bash
python manage.py createsuperuser
```

## Project Structure

```
account/    - authentication app (login, register, password reset, profile)
lms/        - core app (courses, lessons, videos, enrollment, checkout)
templates/  - Django templates (home, courses, auth, partials)
static/     - CSS/JS/images
website/    - project config & settings
```

## Notes

- Sensitive settings are read from environment variables (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `EMAIL_*`).
- **Database**: SQLite is used out of the box. To use PostgreSQL in production, install the driver (`pip install psycopg[binary]`) and set the `DATABASE_URL` env var, e.g. `DATABASE_URL=postgres://user:pass@host:5432/dbname`.
- Media uploads (course images, videos, author profiles) are stored under `media/`.