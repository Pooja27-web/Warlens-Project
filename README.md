# Warlens-Project

WarLens is an NLP-powered news analysis and dataset dashboard built with Flask,
Python, and SQLite. It includes CRUD REST API endpoints and text vectorization
models.

## Deploy on Render

This repository is configured for a direct Render deployment:

1. Connect this GitHub repository to a new Render Web Service.
2. Select the `main` branch.
3. Render will use the root `render.yaml` automatically.
4. If entering commands manually, use:

   - Build command: `pip install -r WARLENS/requirements.txt`
   - Start command: `gunicorn --chdir WARLENS app:app`

The Flask application is located in `WARLENS/`, and Render serves it through
the Gunicorn WSGI entry point `app:app`.
