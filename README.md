# XRWVM Full Stack Developer Capstone

Repository: xrwvm_fullstack_developer_capstone

Project Name: XRWVM Full Stack Developer Capstone

Description
-
This project is a capstone full-stack application demonstrating a Django backend with a React frontend. It implements dealer listings, dealer details with reviews, and a review submission flow. The backend exposes JSON APIs under the `djangoapp` app, and the frontend is a single-page React application served from the `frontend` folder (built assets are placed into `server/frontend/build`).

Key Features
-
- List car dealerships (backend API + React listing page)
- View dealer details and reviews
- Post reviews (authenticated users)
- Simple sentiment analysis integration for reviews

Tech Stack
-
- Backend: Django (Python 3.12)
- Frontend: React (Create React App)
- Database: SQLite (development)

Repository Layout
-
- `server/` — Django project and app code (`djangoproj`, `djangoapp`)
- `frontend/` — React application source and build output

Quick Start (Development)
-
1. Create and activate a Python virtual environment (Windows PowerShell example):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r server/requirements.txt
```

2. Install frontend dependencies and build (from repository root):

```bash
cd frontend
npm install
npm run build
cd ..
```

3. Run Django development server (from `server/`):

```bash
cd server
python manage.py migrate
python manage.py runserver
```

4. Open the app in your browser:

- Main SPA routes are served from Django and include `/dealers/`, `/dealer/<id>/`, and `/postreview/<id>/`.

Backend API Endpoints (examples)
-
- `GET /djangoapp/get_dealers/` — list dealers
- `GET /djangoapp/dealer/<id>/` — dealer details
- `GET /djangoapp/dealer/<id>/reviews` — reviews for a dealer
- `POST /djangoapp/add_review` — submit a new review

Contributing
-
Please open issues or pull requests. Follow PEP8 for Python code and standard ESLint/Prettier conventions for frontend code.

License
-
See the `LICENSE` file at the repository root.
