# Food Waste Reduction Platform

A Flask application for predicting food surplus, recording donations, tracking donation status, and matching donations with NGOs by location.

## Run locally

```bash
python -m venv .venv
```

Activate the virtual environment, then install the dependencies and start the app:

```bash
pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000>.

## Deploy on Render

1. Push this project to a GitHub repository.
2. In Render, create a **Web Service** and connect the repository.
3. Set the build command to `pip install -r requirements.txt`.
4. Set the start command to `gunicorn app:app`.
5. Deploy the service; Render will provide its public URL.

The app uses SQLite. The included local database is excluded from Git, so a deployment creates a fresh database. SQLite data on a free hosting instance may be lost when that instance is replaced or restarted; use persistent storage or a managed database if donation records must be retained.
