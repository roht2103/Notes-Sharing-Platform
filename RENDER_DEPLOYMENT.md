# Render Deployment Guide

## Digital Notes Sharing Platform

Complete step-by-step guide to deploy your Django application on Render.

---

## 📋 **Pre-Deployment Checklist**

Before deploying, you need:

- ✅ A Render account (free tier works fine)
- ✅ Your Django project on GitHub
- ✅ GitHub account
- ✅ Credit card (for Render verification - free tier available, no charges)

---

## 🚀 **STEP 1: Prepare Your Project for Render**

### **1.1: Create/Update requirements.txt**

Make sure your `requirements.txt` includes these packages:

```txt
Django>=5.0,<5.1
Pillow>=10.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
dj-database-url==2.1.0
```

**Why each package?**

- `gunicorn` - Production WSGI server (required on Render)
- `psycopg2-binary` - PostgreSQL database adapter
- `whitenoise` - Serves static files efficiently
- `dj-database-url` - Parses database URLs from environment variables

### **1.2: Create build.sh Script**

Create a file named `build.sh` in your project root:

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create default categories (if they don't exist)
python manage.py shell << END
from notes.models import Category

categories = [
    {'category_name': 'Computer Science', 'description': 'Programming, algorithms, data structures'},
    {'category_name': 'Mathematics', 'description': 'Calculus, algebra, statistics'},
    {'category_name': 'Physics', 'description': 'Mechanics, thermodynamics, quantum physics'},
    {'category_name': 'Chemistry', 'description': 'Organic, inorganic, physical chemistry'},
    {'category_name': 'Business', 'description': 'Management, marketing, finance'},
    {'category_name': 'Engineering', 'description': 'Electrical, mechanical, civil engineering'}
]

for cat in categories:
    Category.objects.get_or_create(**cat)

print("Categories created successfully!")
END

# Create admin user automatically (optional - comment out for security)
# python manage.py create_default_admin
```

**Make it executable:**

```bash
chmod +x build.sh
```

### **1.3: Update settings.py for Production**

Add these configurations to `digital_notes/settings.py`:

**At the top, add imports:**

```python
import os
import dj_database_url
```

**Update ALLOWED_HOSTS:**

```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',  # Allows all Render subdomains
]
```

**Update DEBUG setting (make it environment-dependent):**

```python
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
```

**Update SECRET_KEY (use environment variable):**

```python
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-change-in-production')
```

**Update DATABASES (add PostgreSQL support):**

```python
# Default to SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Override with PostgreSQL if DATABASE_URL is set (production)
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)
```

**Add WhiteNoise middleware (for static files):**

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this line
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... rest of middleware
]
```

**Configure static files (at the bottom):**

```python
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

**Add security settings for production:**

```python
# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

---

## 🚀 **STEP 2: Push to GitHub**

### **2.1: Initialize Git Repository (if not already done)**

```bash
cd "D:\WORKSPACE\Notes Sharing Platform"
git init
git add .
git commit -m "Prepare for Render deployment"
```

### **2.2: Create GitHub Repository**

1. Go to [github.com](https://github.com)
2. Click **"New repository"**
3. Name: `notes-sharing-platform`
4. Keep it **Public** (required for Render free tier)
5. Click **"Create repository"**

### **2.3: Push to GitHub**

```bash
git remote add origin https://github.com/YOUR_USERNAME/notes-sharing-platform.git
git branch -M main
git push -u origin main
```

---

## 🚀 **STEP 3: Create Render Account**

1. Go to [render.com](https://render.com)
2. Click **"Get Started"**
3. Sign up with **GitHub** (recommended - easier deployment)
4. Authorize Render to access your GitHub repositories
5. Verify your email
6. Add payment method (required for verification, free tier available)

---

## 🚀 **STEP 4: Create PostgreSQL Database**

### **4.1: Create Database**

1. From Render Dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. Configure:
   - **Name**: `notes-platform-db`
   - **Database**: `notes_db`
   - **User**: `notes_user` (auto-generated)
   - **Region**: Choose closest to you (e.g., Oregon USA)
   - **PostgreSQL Version**: 16 (latest)
   - **Plan**: **Free** (0.1 GB RAM, 1 GB storage, expires after 90 days)
4. Click **"Create Database"**

### **4.2: Wait for Database Creation**

- Wait 2-3 minutes for database to be ready
- Status will change to **"Available"**

### **4.3: Copy Database Credentials**

Once ready, you'll see:

- **Internal Database URL** (use this for web service)
- **External Database URL** (for local testing)

**Copy the Internal Database URL** - you'll need it in Step 5.

It looks like:

```
postgresql://notes_user:random_password@dpg-xxx-a.oregon-postgres.render.com/notes_db
```

---

## 🚀 **STEP 5: Create Web Service**

### **5.1: Create New Web Service**

1. From Render Dashboard, click **"New +"**
2. Select **"Web Service"**
3. Click **"Build and deploy from a Git repository"**
4. Click **"Connect a repository"**
5. Find and select your **`notes-sharing-platform`** repository
6. Click **"Connect"**

### **5.2: Configure Web Service**

Fill in these settings:

**Basic Settings:**

- **Name**: `notes-sharing-platform` (will become your URL subdomain)
- **Region**: Same as your database (e.g., Oregon USA)
- **Branch**: `main`
- **Root Directory**: Leave blank
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn digital_notes.wsgi:application`

**Instance Type:**

- Select **"Free"** ($0/month)
  - 512 MB RAM
  - Spins down after 15 minutes of inactivity
  - Spins up automatically when accessed (takes 30-60 seconds)

### **5.3: Add Environment Variables**

Scroll down to **"Environment Variables"** section and add these:

| Key              | Value                                          |
| ---------------- | ---------------------------------------------- |
| `DATABASE_URL`   | _Paste your Internal Database URL from Step 4_ |
| `SECRET_KEY`     | _Generate a new secret key (see below)_        |
| `DEBUG`          | `False`                                        |
| `PYTHON_VERSION` | `3.10.0`                                       |

**Generate SECRET_KEY:**
On your local machine, run:

```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
>>> exit()
```

Copy the generated key and paste it as SECRET_KEY value.

### **5.4: Create Web Service**

1. Click **"Create Web Service"**
2. Render will start building your application
3. This takes 5-10 minutes for the first deployment

### **5.5: Monitor Build Process**

Watch the **"Logs"** tab to see:

- Installing dependencies
- Collecting static files
- Running migrations
- Creating categories

If any errors occur, they'll show in the logs.

---

## 🚀 **STEP 6: Configure Static & Media Files**

### **6.1: Verify Static Files**

After successful build, your static files are served by WhiteNoise automatically.

Check in logs for:

```
127 static files copied to '/opt/render/project/src/staticfiles'
```

### **6.2: Media Files (File Uploads)**

⚠️ **Important Limitation**: Render's free tier has **ephemeral storage** - uploaded files will be deleted when the service restarts (every 15 minutes of inactivity).

**Solutions:**

**Option A: Use External Storage (Recommended for Production)**

- Cloudinary (free tier: 25GB storage, 25GB bandwidth/month)
- AWS S3
- Google Cloud Storage

**Option B: Accept the limitation (for testing/demo)**

- Files disappear on restart
- Fine for development/portfolio demos

For now, accept the limitation. We can add Cloudinary later if needed.

---

## 🚀 **STEP 7: Create Admin User**

### **7.1: Access Render Shell**

1. Go to your web service dashboard
2. Click **"Shell"** tab (top right)
3. This opens a terminal connected to your live server

### **7.2: Create Admin User**

In the Render Shell, run:

```bash
# Navigate to project directory
cd /opt/render/project/src

# Create admin user (interactive)
python manage.py createsuperuser
# Enter username: admin
# Enter email: your-email@example.com
# Enter password: (create a strong password)
# Confirm password: (repeat password)
```

Or use the default admin creator:

```bash
python manage.py create_default_admin
# This creates: username=admin, password=admin123
# ⚠️ Change password immediately after first login!
```

---

## 🚀 **STEP 8: Test Your Application**

### **8.1: Get Your URL**

Your app is live at:

```
https://notes-sharing-platform.onrender.com
```

(Replace `notes-sharing-platform` with your service name)

### **8.2: Test All Features**

- ✅ Home page loads (note: first load after inactivity takes 30-60 seconds)
- ✅ Register new account
- ✅ Login
- ✅ View categories
- ✅ Upload a note (test file upload)
- ✅ View note details
- ✅ Download note
- ✅ Add comment
- ✅ Admin panel: `/admin`
  - Login with your admin credentials
  - Verify all models appear

### **8.3: Performance Note**

Free tier limitations:

- **Cold start**: 30-60 seconds after 15 minutes of inactivity
- **Active performance**: Fast and responsive
- **Spins down**: After 15 minutes of no requests
- **Database**: Expires after 90 days (can create a new one)

---

## 🐛 **Troubleshooting Common Issues**

### **Issue 1: Build Failed - "Permission denied: build.sh"**

**Solution:**

```bash
# On your local machine
chmod +x build.sh
git add build.sh
git commit -m "Make build.sh executable"
git push
```

Render will auto-deploy the fix.

### **Issue 2: "DisallowedHost" Error**

**Solution:**
Check `settings.py` has:

```python
ALLOWED_HOSTS = ['.onrender.com']
```

Then:

```bash
git add digital_notes/settings.py
git commit -m "Fix ALLOWED_HOSTS"
git push
```

### **Issue 3: Static Files Not Loading (No CSS)**

**Solution:**

1. Verify `whitenoise` is in `requirements.txt`
2. Check middleware includes `WhiteNoiseMiddleware`
3. Check build logs show "static files copied"
4. Hard refresh: Ctrl + F5

### **Issue 4: "ModuleNotFoundError: No module named 'gunicorn'"**

**Solution:**
Add to `requirements.txt`:

```
gunicorn==21.2.0
```

Push to GitHub - Render will redeploy automatically.

### **Issue 5: Database Connection Error**

**Solution:**

1. Check DATABASE_URL environment variable is set correctly
2. Verify database status is "Available"
3. Check `psycopg2-binary` is in `requirements.txt`
4. Try recreating the database

### **Issue 6: Site Takes Forever to Load**

**Cause:** Cold start after inactivity (free tier limitation)

**Solution:** Options:

1. Accept 30-60 second cold start (normal for free tier)
2. Upgrade to paid tier (keeps service always running)
3. Use a service like UptimeRobot to ping your site every 14 minutes

### **View Logs**

If something goes wrong:

1. Go to your web service dashboard
2. Click **"Logs"** tab
3. Look for error messages
4. Check both **"Build Logs"** and **"Runtime Logs"**

---

## 🔄 **Deploy Updates**

### **Method 1: Automatic Deployment (Recommended)**

1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your changes"
   git push
   ```
3. Render automatically detects the push and redeploys (takes 3-5 minutes)

### **Method 2: Manual Deployment**

1. Go to your web service dashboard
2. Click **"Manual Deploy"**
3. Select branch: `main`
4. Click **"Deploy latest commit"**

### **After Database/Model Changes:**

If you changed models:

```bash
# Local machine
python manage.py makemigrations
git add .
git commit -m "Add new migrations"
git push
```

Render will automatically run migrations during build (it's in `build.sh`).

---

## 🔒 **Security Improvements**

### **1. Change Admin Password**

If you used `create_default_admin`:

1. Go to `/admin`
2. Login with `admin` / `admin123`
3. Click your username → Change password
4. Set a strong password

### **2. Set DEBUG=False**

Ensure environment variable `DEBUG` is set to `False` in production.

### **3. Rotate SECRET_KEY**

Generate a new SECRET_KEY periodically:

1. Go to web service → Environment
2. Click "Edit" next to SECRET_KEY
3. Generate and paste new key
4. Click "Save Changes"
5. Service will auto-restart

### **4. Enable HTTPS (Already Enabled)**

Render provides free SSL certificates automatically.

---

## 📊 **Monitoring**

### **Check Metrics:**

From your web service dashboard:

- **Metrics** tab: CPU, Memory, Response time
- **Logs** tab: Real-time logs
- **Events** tab: Deployment history

### **Free Tier Limits:**

- **RAM**: 512 MB
- **Bandwidth**: 100 GB/month
- **Build minutes**: 500 minutes/month
- **Database**: 1 GB storage, expires after 90 days

---

## 🎁 **Optional: Add Custom Domain**

### **Free Subdomain (Included):**

```
https://your-service-name.onrender.com
```

### **Custom Domain (Optional):**

1. Go to web service → Settings
2. Click **"Add Custom Domain"**
3. Enter your domain: `notes.yourdomain.com`
4. Render will provide DNS records
5. Add these records to your domain registrar:
   - Type: `CNAME`
   - Name: `notes`
   - Value: `your-service-name.onrender.com`
6. Wait for DNS propagation (5-30 minutes)
7. Render auto-provisions SSL certificate

Custom domains require a paid plan ($7/month).

---

## 🆙 **Upgrade to Paid Plan (Optional)**

**Starter Plan - $7/month per service:**

- 512 MB RAM (same as free)
- No spin down (always running)
- No cold starts
- Priority support

**Standard Plan - $25/month:**

- 2 GB RAM
- Always running
- Background workers
- Better performance

**Database Plans:**

- **Starter**: $7/month (1 GB storage)
- **Standard**: $20/month (10 GB storage)

---

## 💡 **Pro Tips**

### **1. Keep Your Site Awake (Free Tier)**

Use [UptimeRobot](https://uptimerobot.com) (free):

- Create monitor for your Render URL
- Set interval: 14 minutes
- Prevents cold starts by pinging your site regularly

### **2. Optimize Cold Start Time**

In `build.sh`, reduce unnecessary operations:

- Comment out category creation if already done
- Skip creating default admin

### **3. Monitor Database Size**

Free database: 1 GB limit

```bash
# In Render Shell
python manage.py shell
>>> from django.db import connection
>>> cursor = connection.cursor()
>>> cursor.execute("SELECT pg_size_pretty(pg_database_size('notes_db'));")
>>> print(cursor.fetchone()[0])
```

### **4. Backup Your Database**

Render provides snapshots (paid plans) or use:

```bash
# In Render Shell
python manage.py dumpdata > backup.json
# Download from Files section
```

---

## 🎉 **Success!**

Your Django Notes Sharing Platform is now live at:
**`https://your-service-name.onrender.com`**

Share this URL with others!

---

## 📚 **Next Steps**

1. ✅ Change default admin password
2. ✅ Test all features thoroughly
3. ✅ Upload sample notes
4. ✅ Share your live URL!
5. ✅ Consider UptimeRobot to prevent cold starts
6. ✅ Set up Cloudinary for persistent file uploads (optional)

---

## 🆘 **Need Help?**

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Render Community**: [community.render.com](https://community.render.com)
- **Django Docs**: [docs.djangoproject.com](https://docs.djangoproject.com)

---

## 📋 **Quick Command Reference**

```bash
# Local development
python manage.py runserver
python manage.py makemigrations
python manage.py migrate

# Render Shell (production)
cd /opt/render/project/src
python manage.py createsuperuser
python manage.py migrate
python manage.py collectstatic

# Git deployment
git add .
git commit -m "Your message"
git push  # Auto-deploys to Render
```

---

**Deployment Date**: March 4, 2026  
**Django Version**: 5.0.14  
**Python Version**: 3.10  
**Platform**: Render  
**Database**: PostgreSQL 16
