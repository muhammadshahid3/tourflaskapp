# Wanderly — Flask Tour Booking System

A production-style tour booking web application built with Flask, SQLAlchemy,
Flask-Login, Bootstrap 5, and MySQL (AWS RDS), containerized with Docker.

## Tech Stack

- **Backend:** Flask (application factory + Blueprints)
- **Database:** MySQL on AWS RDS
- **ORM:** SQLAlchemy + Flask-Migrate
- **Auth:** Flask-Login (separate Admin and User accounts)
- **Forms:** Flask-WTF (CSRF protected)
- **Frontend:** Bootstrap 5, Jinja2, Chart.js (reports)
- **Containerization:** Docker + Docker Compose (Flask app only — the
  database is your existing AWS RDS instance, not a container)

## Features

- Modern travel landing page (hero, search, categories, featured
  destinations, popular tours, testimonials, why-choose-us, footer)
- Separate **User** and **Admin** auth flows (sign up, login, logout,
  change password; users also get "forgot password")
- Admin dashboard with stat cards and sidebar navigation
- Full CRUD for Categories, Destinations, and Tours (with image uploads)
- Booking management: confirm / cancel / mark completed
- User management: view / block / activate / delete
- Reports: revenue & bookings trend, most booked tours, popular
  destinations
- User side: browse/search/filter tours, view details, book a tour,
  booking history, cancel pending bookings, edit profile & password

## Project Structure

```
tour_booking/
├── app/
│   ├── auth/            # Admin + User authentication routes
│   ├── admin/            # Admin dashboard, CRUD, reports
│   ├── user/              # User dashboard, browsing, booking
│   ├── main/              # Public landing page & search
│   ├── models/            # SQLAlchemy models
│   ├── templates/         # Jinja2 templates
│   ├── static/             # css/js/images
│   ├── forms.py
│   ├── decorators.py       # admin_required / user_required
│   ├── extensions.py
│   └── __init__.py         # app factory
├── migrations/              # Flask-Migrate (created after `flask db init`)
├── config.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── run.py
└── README.md
```

## Running with Docker Compose (AWS RDS)

1. Create a MySQL 8 database on AWS RDS and note the endpoint, port,
   database name, username, and password. Make sure its security group
   allows inbound connections from wherever this container will run.

2. Copy the environment template and fill in your RDS details:

   ```bash
   cp .env.example .env
   ```

   ```env
   DB_HOST=your-db-instance.xxxxxxxxxx.us-east-1.rds.amazonaws.com
   DB_PORT=3306
   DB_NAME=tour_booking
   DB_USER=admin
   DB_PASSWORD=your_password
   SECRET_KEY=change_me_to_a_long_random_string
   ```

3. Build and start the app:

   ```bash
   docker compose up --build
   ```

   This starts **only** the Flask container — it connects directly to
   your AWS RDS instance over the network using the `DB_*` variables.
   On first boot the app automatically creates all tables
   (`db.create_all()`) and seeds one default admin account using the
   `DEFAULT_ADMIN_*` variables in `.env` (default:
   `admin@example.com` / `Admin@123` — **change this immediately**).

4. Visit `http://localhost:5000`.

### Using Flask-Migrate instead of auto-create (optional, recommended for production)

The app calls `db.create_all()` on startup for convenience. For a real
production workflow, disable that in `app/__init__.py` and instead run:

```bash
docker compose exec web flask db init
docker compose exec web flask db migrate -m "initial schema"
docker compose exec web flask db upgrade
```

## Running locally without Docker

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then edit .env with your RDS details
flask --app run.py run --debug
```

## Default Admin Login

| Field    | Value                                   |
|----------|------------------------------------------|
| Email    | value of `DEFAULT_ADMIN_EMAIL` in `.env` |
| Password | value of `DEFAULT_ADMIN_PASSWORD`        |

Change the password immediately from **Admin Panel → Change Password**,
or set your own values in `.env` before first startup.

## Booking Flow

```
User selects a tour → views details → chooses number of persons →
confirms booking → booking saved with status "Pending" →
Admin reviews it in Admin Panel → Bookings → Confirm/Cancel →
Admin marks "Completed" once the trip has taken place
```

## Notes

- "Forgot Password" is intentionally simple (email + new password, no
  email delivery) as requested — this is fine for a demo/prototype but
  should be replaced with a token-based email reset flow before any
  real production use.
- Uploaded images are stored on a Docker named volume
  (`uploads_data`) so they persist across container rebuilds.
- No Kubernetes, Nginx, CI/CD, Redis, or Celery are used, per the
  project requirements.
# tourflaskapp
