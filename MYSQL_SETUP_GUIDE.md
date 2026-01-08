# MySQL Setup Guide for Fitness Tracker

## 🗄️ Setting Up MySQL Database

### Prerequisites:
1. **MySQL Workbench** installed and running
2. **MySQL Server** running on localhost:3306

### Step 1: Configure MySQL User
Open MySQL Workbench and run these commands:

```sql
-- Create database
CREATE DATABASE IF NOT EXISTS fitness_tracker_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Create a user for the application (optional, safer than using root)
CREATE USER IF NOT EXISTS 'fitness_user'@'localhost' IDENTIFIED BY 'fitness123';

-- Grant privileges
GRANT ALL PRIVILEGES ON fitness_tracker_db.* TO 'fitness_user'@'localhost';
FLUSH PRIVILEGES;

-- Show databases to verify
SHOW DATABASES;
```

### Step 2: Update Django Settings
In `settings.py`, you have these options:

#### Option A: Use dedicated user (recommended)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fitness_tracker_db',
        'USER': 'fitness_user',
        'PASSWORD': 'fitness123',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

#### Option B: Use root user with password
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fitness_tracker_db',
        'USER': 'root',
        'PASSWORD': 'your_root_password',  # Set your actual password
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

### Step 3: Run Django Migrations
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 🔧 Troubleshooting:

#### Error: "Access denied for user 'root'@'localhost'"
- **Solution 1:** Set a password for root user in MySQL Workbench
- **Solution 2:** Create a dedicated user as shown above
- **Solution 3:** Use MySQL Workbench → Users and Privileges → Add Account

#### Error: "Can't connect to MySQL server"
- Check if MySQL service is running
- Verify port 3306 is open
- Make sure MySQL Workbench can connect

#### Error: "Unknown database 'fitness_tracker_db'"
- Run the CREATE DATABASE command in MySQL Workbench
- Make sure the database name matches exactly

### 📋 Quick Commands for MySQL Workbench:
```sql
-- Check if database exists
SHOW DATABASES;

-- Check users
SELECT user, host FROM mysql.user;

-- Check privileges
SHOW GRANTS FOR 'fitness_user'@'localhost';
```

### 🔙 Rollback to SQLite:
If you want to switch back to SQLite, just uncomment the SQLite section in settings.py and comment out the MySQL section.