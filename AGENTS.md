# Project agent memory

This file is the project's committed home for project-intrinsic agent knowledge: build, test, release, architecture, and sharp-edge notes that should travel with the code.

- Add durable project-specific notes here as they are discovered through real work.

## Project notes

- Demo for django-erp-framework + django-slick-reporting + django-jazzy-tabler (the theme is part of the showcase; jazzy-tabler replaced jazzmin).
- `requirements.txt`: erp-framework is pinned from the git release tag `v1.6.0`, not PyPI — PyPI sdists up to 1.5.2 ship no templates/static, so the erp pages 500 without them. Move back to a PyPI pin only after verifying a release ships its templates.
- erp-framework v1.6.0's `jazzy_tabler_integration` ships a `jazzy_tabler/includes/sidebar_bottom.html` that loads a nonexistent `erp_tags` library; `templates/jazzy_tabler/includes/sidebar_bottom.html` in this repo overrides it. Drop the override only after upstream fixes the load line.
- Report registry namespaces come from `base_model._meta.model_name` (or the module name when no `base_model`), so `{% get_report base_model=... %}` in `templates/` must use that namespace (e.g. `product.productmovementstatement`, not `purchase...`). Inspect `erp_framework.reporting.registry.report_registry._store` for the live keys.
- Settings follow the deployment contract documented in `README.md` / `.env.example`: env-driven via django-environ, sqlite fallback when `POSTGRES_DB` is unset, behind-proxy HTTPS settings always on.
- Seed the demo with `python manage.py seed_demo` (creates the `test`/`testuser123` superuser, then wraps `create_entries` + `create_purchase_entries`); smoke tests: `python manage.py test` (see `my_shop/tests.py`).

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this project.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.
