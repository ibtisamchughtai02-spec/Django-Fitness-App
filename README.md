# 🏋️ Fitness Tracker & Workout Management System

A comprehensive Django web application for tracking fitness workouts, exercises, and progress with a focus on security, data integrity, and user experience.

## 📋 Project Overview

This is a full-stack fitness tracking application built with Django 6.0 and MySQL, demonstrating:
- **Django MVT Architecture** with clear separation of concerns
- **Secure CRUD Operations** with CSRF protection, XSS prevention, and SQL injection protection
- **Data Import/Export** supporting CSV, JSON, and text file formats
- **Advanced Features** including Django signals, database indexes, and ORM optimization
- **Professional UI** with Bootstrap 5, responsive design, and intuitive navigation

## 🎯 Features

### Core Functionality
- **User Authentication & Authorization**
  - Secure registration and login
  - Password validation with Django validators
  - Profile management with BMI calculation

- **Workout Management**
  - Create, read, update, delete workouts
  - Multiple workout types (cardio, strength, flexibility, sports, mixed)
  - Track duration, calories burned, and notes
  - Date-based filtering and search

- **Exercise Tracking**
  - Add exercises to workouts
  - Track sets, reps, weight, and rest time
  - Exercise categories (chest, back, legs, core, etc.)
  - Calculate total volume and track bodyweight exercises

- **Progress Analytics**
  - Dashboard with statistics (total workouts, calories, duration)
  - Weekly progress tracking
  - Workout type distribution
  - Exercise frequency leaderboard

- **Data Management**
  - Import workouts from CSV, JSON, or text files
  - Export data in multiple formats
  - File validation and error handling

## 🛠️ Technology Stack

- **Backend:** Django 6.0, Python 3.13
- **Database:** MySQL 8.0 (local) / PostgreSQL (production)
- **Frontend:** Bootstrap 5, Font Awesome, Custom CSS
- **Deployment:** Render (with Gunicorn & WhiteNoise)
- **Security:** CSRF protection, XSS prevention, ORM-based queries

## 🔒 Security Implementation

### 1. **CSRF Protection**
- Django CSRF middleware enabled
- CSRF tokens in all forms
- `@csrf_protect` decorators on sensitive views

### 2. **XSS Prevention**
- Automatic template escaping
- `escapejs` filter for JavaScript contexts
- Safe rendering of user-generated content

### 3. **SQL Injection Prevention**
- 100% Django ORM usage
- No raw SQL queries
- Parameterized queries via ORM

### 4. **Authentication & Authorization**
- `@login_required` decorators on all sensitive views
- User-based data filtering
- Session-based authentication

### 5. **Password Security**
- PBKDF2 hashing algorithm
- Multiple password validators (length, similarity, common passwords, numeric)
- Secure password comparison

### 6. **Input Validation**
- Model-level validators (MinValueValidator, MaxValueValidator)
- Form-level validation with custom clean methods
- File upload validation (size limits, type checking)

## 📊 Database Design

### Models & Relationships

```
User (Django built-in)
  ↓ (1:1)
UserProfile
  - age, weight, height
  - activity_level, fitness_goal
  - BMI calculation

User
  ↓ (1:*)
Workout
  - name, workout_type, date
  - duration, calories_burned
  ↓ (1:*)
  Exercise
    - exercise_name, category
    - sets, reps, weight
```

### Data Integrity
- **Domain Integrity:** Field validators, choice fields, data type constraints
- **Entity Integrity:** Primary keys, unique constraints, indexes
- **Referential Integrity:** Foreign keys with CASCADE delete, related_name navigation

### Performance Optimization
- 8 database indexes across models
- Composite indexes on frequently queried fields
- Query optimization with `prefetch_related()` and `select_related()`

## 🔧 Django Signals (Trigger Equivalents)

1. **Auto-create UserProfile** - Creates profile when user registers
2. **Auto-calculate Calories** - Estimates calories based on workout type/duration
3. **Update Workout Timestamp** - Updates workout when exercises change
4. **Deletion Logging** - Logs workout/exercise deletions for audit
5. **Milestone Tracking** - Tracks workout and calorie milestones

## 📂 Project Structure

```
FitnessApp/
├── fitness_project/          # Django project settings
│   ├── settings.py          # Configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI application
├── fitness_tracker/          # Main app
│   ├── models.py            # Data models
│   ├── views.py             # Business logic
│   ├── forms.py             # Form validation
│   ├── signals.py           # Database triggers
│   ├── data_utils.py        # Import/export utilities
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, images
├── requirements.txt         # Python dependencies
├── build.sh                 # Render build script
├── Procfile                 # Render process file
└── manage.py                # Django management
```

## 🚀 Installation & Setup

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/ibtisamchughtai02-spec/Django-Fitness-App.git
cd Django-Fitness-App
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup MySQL database**
- Create database: `fitness_tracker_db`
- Update credentials in `settings.py`

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Collect static files**
```bash
python manage.py collectstatic
```

8. **Run development server**
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

## 🌐 Deployment (Render)

### Prerequisites
- GitHub repository
- Render account
- PostgreSQL database on Render

### Deployment Steps

1. **Push to GitHub**
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

2. **Create Web Service on Render**
- Connect GitHub repository
- Build Command: `./build.sh`
- Start Command: (auto-detected from Procfile)

3. **Add PostgreSQL Database**
- Create PostgreSQL database on Render
- Copy `DATABASE_URL` to environment variables

4. **Configure Environment Variables**
```
DATABASE_URL=<your-postgres-url>
DJANGO_SECRET_KEY=<your-secret-key>
DEBUG=False
```

5. **Deploy!**
- Render will automatically build and deploy

## 📝 API Endpoints

### Authentication
- `POST /register/` - User registration
- `POST /login/` - User login
- `GET /logout/` - User logout

### Workouts
- `GET /workouts/` - List all workouts
- `POST /workouts/create/` - Create workout
- `GET /workouts/<id>/` - View workout details
- `POST /workouts/<id>/edit/` - Edit workout
- `POST /workouts/<id>/delete/` - Delete workout

### Exercises
- `POST /workouts/<id>/exercises/create/` - Add exercise
- `POST /exercises/<id>/edit/` - Edit exercise
- `POST /exercises/<id>/delete/` - Delete exercise

### Data Management
- `GET /import/` - Import data form
- `POST /import/` - Process import
- `GET /export/?format=csv` - Export as CSV
- `GET /export/?format=json` - Export as JSON
- `GET /export/?format=txt` - Export as text

## 👥 Contributing

This is an academic project for CPAN 214 - Advanced Python with Django.

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Authors

- **Developer:** Ibtisam Chughtai
- **Course:** CPAN 214 - Advanced Python with Django
- **Institution:** Humber College
- **Date:** January 2026

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap 5 Framework
- Font Awesome Icons
- Humber College CPAN 214 Course Materials

## 📞 Support

For questions or issues, please open an issue on GitHub or contact through the repository.

---

**Built with ❤️ using Django MVT Architecture**
