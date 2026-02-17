# Django Rest API

## Endpoints for testing

* `/restaurant/bookings/`
* `/restaurant/menu/`

## Configuration / Run

1. Create an environment file from the template:

   ```bash
   cp .env.example .env
   ```

2. Fill in `.env` values:

   - `SECRET_KEY` — Django secret key.
   - `DEBUG` — `True`/`False` debug mode flag.
   - `DB_NAME` — MySQL database name.
   - `DB_USER` — MySQL user.
   - `DB_PASSWORD` — MySQL password.
   - `DB_HOST` — MySQL host.
   - `DB_PORT` — MySQL port.

3. Export variables from `.env` (example for bash):

   ```bash
   set -a
   source .env
   set +a
   ```

4. Run migrations and start the server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

> If MySQL variables are not provided, the project falls back to SQLite (`db.sqlite3`) for local development.
