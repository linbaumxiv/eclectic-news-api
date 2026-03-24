### 📰 Eclectic News API 📰
A high-performance, role-based news dissemination engine built with Django REST Framework. Featuring automated editorial workflows, many-to-many subscription logic, and multi-channel dissemination (Email & X/Twitter) for a modern news platform.

### 🚀 Key Features
Personalized Feed: Users receive a custom news feed based on their subscriptions to Journalists or Publications using complex OR logic queries.

Social Integration: Automated X (Twitter) dissemination via Tweepy and Django post_save signals.

Newsletter System: Automated email alerts to subscribers when new articles are approved.

Production-Grade DB: Fully migrated to MariaDB for high concurrency and data integrity.

Granular RBAC: Distinct permissions for Readers, Journalists, and Editors.

Admin Excellence: Enhanced dashboard with bulk actions and horizontal relation filters.

Professional Documentation: Full API and codebase documentation generated via Sphinx.

Containerized: Ready for deployment on any system via Docker.

### 🛠 Tech Stack
Backend: Django 5.x+ / Django REST Framework

Database: MariaDB 11.x (Production) / SQLite (Testing)

DevOps: Docker, Sphinx(Documentation)

Third-Party: Tweepy (X API v2), Python-Dotenv

Integration: Django Core Mail (SMTP)

Testing: Django TestCase (Unit & Integration)

### 🔗 Key Endpoints
/api/articles/feed/ - Personalized user news feed.

/api/subscriptions/ - Manage follows for journalists/publications.

/api/articles/ - Full article archives with metadata filtering.

### 🏗 System Architecture (3NF)

The schema is engineered for data integrity. By utilizing a Custom User Model with self-referential Many-to-Many relationships for subscriptions, we eliminated the need for redundant tables, achieving Third Normal Form (3NF).

### 🏗 Installation & Setup

1. Clone the Repository

Bash:
git clone https://github.com/linbaumxiv/eclectic-news-api.git
cd eclectic-news-api

2. Configure Environment (Crucial)

For security, sensitive credentials are not tracked by Git. Create a .env file in the root directory:

Plaintext:
DB_NAME=eclectic_news
DB_USER=eclectic_admin
DB_PASSWORD=your_actual_password
DB_HOST=127.0.0.1 (or 'db' if using Docker)
X_API_KEY=your_keys
SECRET_KEY=your_django_secret_key

### 🐳 Running with Docker (Recommended)

This is the fastest way to ensure the app works regardless of your local Python or Database setup.

1.Build the Image:

Bash:
docker build -t eclectic-news .

2. Run the Container:

Bash:
docker run -p 8000:8000 --env-file .env eclectic-news
The app will be available at http://localhost:8000.

### 🐍 Running with Virtual Environment (Local Dev)

1. Install Dependencies:

Bash:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Database Migration:
Ensure MariaDB is running locally and matches your .env settings, then:

Bash:
python3 manage.py migrate
python3 manage.py runserver

### 📚 Documentation (Sphinx)

The project includes a comprehensive documentation suite. To view the technical docs:

1. Navigate to the docs folder: cd docs

2. Build the HTML files: sphinx-build -b html . _build

3. Open docs/_build/html/index.html in your browser.

### 🧠 System Architecture & 3NF

The schema is engineered for data integrity. By utilizing a Custom User Model with self-referential Many-to-Many relationships for subscriptions, we eliminated the need for redundant tables, achieving Third Normal Form (3NF).

### 🧪 Quality Assurance

Run the test suite to verify logic:

Bash:
python3 manage.py test eclectic

-test_unapproved_hidden: Ensures unapproved content never leaks.

-test_journalist_self_approval: Validates defensive logic.

-test_feed_filtering: Confirms personalization accuracy.