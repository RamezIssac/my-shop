# my-shop

A Django ERP framework example project — the public demo for
[django-erp-framework](https://github.com/RamezIssac/django-erp-framework),
[django-slick-reporting](https://github.com/ra-systems/django-slick-reporting)
and [django-jazzy-tabler](https://pypi.org/project/django-jazzy-tabler/).

This is the code for the demo site at my-shop.django-erp.com.

## Quickstart (local development)

Requires Python 3.10+.

```bash
git clone <repo> && cd my-shop
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

`seed_demo` creates the demo login and all sample data (it wraps the
`create_entries` / `create_purchase_entries` app commands). Log in with
username `test`, password `testuser123` — no `createsuperuser` needed.

No `.env` is needed for local development: without one you get DEBUG off,
an sqlite database, `ALLOWED_HOSTS=127.0.0.1,localhost` and a built-in
development `SECRET_KEY`.

Then browse:

* `/` — the ERP admin site (jazzy-tabler-themed) with the dashboard and reports
* `/admin/` — the stock Django admin
* `/requests-dashboard/` — request analytics reports
* `/front-end-dashboard/` — a sample front-end dashboard page

Run the smoke tests with `python manage.py test`.

## Configuration (.env)

Settings are read from the environment; a `.env` file placed next to
`manage.py` is loaded automatically. See `.env.example` for the full list.

| Variable | Purpose | Default |
| --- | --- | --- |
| `SECRET_KEY` | Django secret key | built-in dev-only value |
| `DEBUG` | debug mode, cast to bool | `false` |
| `ALLOWED_HOSTS` | comma-separated hosts | `127.0.0.1,localhost` |
| `POSTGRES_DB` | when set, Postgres is used | unset → sqlite |
| `POSTGRES_USER` / `POSTGRES_PASSWORD` | Postgres credentials | — |
| `POSTGRES_HOST` / `POSTGRES_PORT` | Postgres location | `127.0.0.1` / `5432` |
| `REDIS_URL` | cache backend location | unset → local memory |
| `STATIC_ROOT` / `MEDIA_ROOT` | collected static / uploads | `./collected_static` / `./media` |

`STATIC_URL` is `/static/` and `MEDIA_URL` is `/media/`.
For deployment behind a proxy terminating HTTPS (e.g. Cloudflare),
`CSRF_TRUSTED_ORIGINS` is derived as `https://<host>` for each allowed host,
and `SECURE_PROXY_SSL_HEADER` / `USE_X_FORWARDED_HOST` are already set.

For production: `pip install -r requirements.txt`, write a real `.env`,
then `python manage.py migrate && python manage.py collectstatic`. The
serving layer is provided by the fleet host: rambo deploys this app with
uWSGI (wsgi module `my_shop.wsgi`) and Daphne (asgi `my_shop.asgi`), the
same as the other fleet apps — no WSGI/ASGI server is pinned here.
