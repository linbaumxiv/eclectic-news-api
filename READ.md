### 📰 Eclectic News API 📰
A high-performance, role-based news dissemination engine built with Django REST Framework. Featuring automated editorial workflows, many-to-many subscription logic, and multi-channel dissemination (Email & X/Twitter) for a modern news platform.

### 🚀 Key Features
Personalized Feed: Users receive a custom news feed based on their subscriptions to Journalists or Publications using complex OR logic queries.

Social Integration: Automated X (Twitter) dissemination via Tweepy and Django post_save signals.

Newsletter System: Automated email alerts to subscribers when new articles are approved.

Production-Grade DB: Fully migrated to MariaDB for high concurrency and data integrity.

Granular RBAC: Distinct permissions for Readers, Journalists, and Editors.

Admin Excellence: Enhanced dashboard with bulk actions and horizontal relation filters.

### 🛠 Tech Stack
Backend: Django 5.x+ / Django REST Framework

Database: MariaDB 11.x (Production) / SQLite (Testing)

Third-Party: Tweepy (X API v2), Python-Dotenv

Integration: Django Core Mail (SMTP)

Testing: Django TestCase (Unit & Integration)

### 🔗 Key Endpoints
/api/articles/feed/ - Personalized user news feed.

/api/subscriptions/ - Manage follows for journalists/publications.

/api/articles/ - Full article archives with metadata filtering.

### 🏗 System Architecture (3NF)

The schema is engineered for data integrity. By utilizing a Custom User Model with self-referential Many-to-Many relationships for subscriptions, we eliminated the need for redundant tables, achieving Third Normal Form (3NF).

### 🛠 Installation & Setup

1.Clone the Repository

Bash:
git clone https://github.com/yourusername/eclectic-news.git
cd eclectic-news

2.Database Setup (MariaDB)

SQL:
CREATE DATABASE eclectic_news CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'eclectic_admin'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON eclectic_news.* TO 'eclectic_admin'@'localhost';

3.Configure Environment
Create a .env file in the root directory:

Code snippet:
DB_NAME=eclectic_news
DB_USER=eclectic_admin
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
X_API_KEY=your_keys

4.Build & Run

Bash:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver

### 🧠 Technical Challenges & Solutions

The MariaDB Migration: Migrated from SQLite to MariaDB to support production workloads. Solved macOS-specific socket connection hurdles (Errcode 13) by reconfiguring directory permissions and forcing TCP/IP connections via 127.0.0.1.

Race Conditions in Signals: Implemented decoupled signal logic to ensure that social media dissemination only triggers after a successful database commit.

Recursive Subscriptions: Leveraged Django's self Many-to-Many relationship on the User model to allow Readers to follow Journalists without creating extraneous join tables.

### 🧪 Quality Assurance

Bash:
python3 manage.py test eclectic

Test Case:	-Description
test_unapproved_hidden:	-Ensures unapproved content never leaks to reader feeds.
test_journalist_self_approval:	-Validates defensive logic preventing unauthorized approval.
test_feed_filtering:	-Confirms M2M logic accurately personalizes content.

### Database Migration & Scaling:
The application has been migrated from SQLite to MariaDB to support concurrent connections and production-level data integrity. I implemented utf8mb4 encoding to support full Unicode (essential for modern global news content) and used environment-based configuration to ensure security and portability across deployment environments.


