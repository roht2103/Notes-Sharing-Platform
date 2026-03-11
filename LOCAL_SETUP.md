# LOCAL SETUP GUIDE - New Laptop/Machine

## Setup Django Notes Sharing Platform from Scratch

Complete step-by-step guide to run this project on a new computer.

---

## 📋 **PREREQUISITES**

Before you start, make sure you have:

### **1. Python 3.10 or Higher**

**Check if Python is installed:**

```bash
python --version
```

**If not installed:**

- **Windows**: Download from [python.org](https://www.python.org/downloads/)
  - ⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation
- **Mac**: `brew install python@3.10`
- **Linux**: `sudo apt install python3.10 python3-pip`

### **2. Git (Optional - for cloning from GitHub)**

**Check if Git is installed:**

```bash
git --version
```

**If not installed:**

- **Windows**: Download from [git-scm.com](https://git-scm.com/)
- **Mac**: `brew install git`
- **Linux**: `sudo apt install git`

---

## 🚀 **SETUP STEPS**

### **Method 1: Clone from GitHub (If Project is on GitHub)**

#### **Step 1: Clone Repository**

```bash
# Navigate to where you want the project
cd C:\Users\YourName\Documents  # Windows
cd ~/Documents  # Mac/Linux

# Clone the repository
git clone https://github.com/YOUR_USERNAME/notes-sharing-platform.git

# Enter project directory
cd notes-sharing-platform
```

---

### **Method 2: Copy Project Files**

#### **Step 1: Transfer Files**

- Copy the entire project folder to your new laptop
- Use USB drive, cloud storage, or any transfer method
- Place it in a convenient location (e.g., Documents folder)

#### **Step 2: Open Project**

```bash
# Navigate to project directory
cd "path/to/Notes Sharing Platform"
```

---

## ⚙️ **AUTOMATED SETUP (RECOMMENDED)**

### **Windows:**

1. **Open Command Prompt or PowerShell** in project directory:
   - Right-click folder → "Open in Terminal"
   - Or: Shift + Right-click → "Open PowerShell window here"

2. **Run setup script:**

   ```cmd
   setup.bat
   ```

3. **Follow the prompts:**
   - Wait for dependencies to install
   - Create admin username and password when prompted
   - Press Enter to continue

4. **Create categories:**

   ```cmd
   venv\Scripts\activate
   python manage.py shell < create_categories.py
   ```

5. **Run the server:**

   ```cmd
   python manage.py runserver
   ```

6. **Open your browser:**
   - Visit: `http://127.0.0.1:8000/`
   - Admin: `http://127.0.0.1:8000/admin/`

---

### **Mac/Linux:**

1. **Open Terminal** in project directory:

   ```bash
   cd "/path/to/Notes Sharing Platform"
   ```

2. **Make setup script executable:**

   ```bash
   chmod +x setup.sh
   ```

3. **Run setup script:**

   ```bash
   ./setup.sh
   ```

4. **Follow the prompts:**
   - Wait for dependencies to install
   - Create admin username and password when prompted

5. **Create categories:**

   ```bash
   source venv/bin/activate
   python manage.py shell < create_categories.py
   ```

6. **Run the server:**

   ```bash
   python manage.py runserver
   ```

7. **Open your browser:**
   - Visit: `http://127.0.0.1:8000/`
   - Admin: `http://127.0.0.1:8000/admin/`

---

## 🔧 **MANUAL SETUP (If Automated Fails)**

### **Step 1: Create Virtual Environment**

**Windows:**

```cmd
python -m venv venv
```

**Mac/Linux:**

```bash
python3 -m venv venv
```

### **Step 2: Activate Virtual Environment**

**Windows (CMD):**

```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

_If you get an error about execution policy, run:_

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

You should see `(venv)` at the start of your command line.

### **Step 3: Install Dependencies**

```bash
pip install -r requirements.txt
```

**Expected packages:**

- Django>=5.0,<5.1
- Pillow>=10.0.0
- gunicorn==21.2.0
- psycopg2-binary==2.9.9
- whitenoise==6.6.0
- dj-database-url==2.1.0

### **Step 4: Run Database Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the SQLite database with all tables.

### **Step 5: Create Admin User**

```bash
python manage.py createsuperuser
```

Enter:

- Username (e.g., admin)
- Email (e.g., admin@example.com)
- Password (min 8 characters)
- Confirm password

### **Step 6: Create Categories**

```bash
python manage.py shell < create_categories.py
```

This creates 6 default categories:

- Computer Science
- Mathematics
- Physics
- Chemistry
- Business
- Engineering

Or use the alternative command:

```bash
python manage.py create_default_admin
```

### **Step 7: Run Development Server**

```bash
python manage.py runserver
```

Server will start at: `http://127.0.0.1:8000/`

### **Step 8: Access the Application**

Open your browser and visit:

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Register**: http://127.0.0.1:8000/register/
- **Login**: http://127.0.0.1:8000/login/

---

## 🧪 **VERIFY SETUP**

### **Quick Test Checklist:**

1. ✅ **Homepage loads** - Shows "Digital Notes Sharing Platform"
2. ✅ **Register** - Create a test account
3. ✅ **Login** - Login with test account
4. ✅ **Categories visible** - See 6 categories in dropdown
5. ✅ **Upload note** - Try uploading a PDF/DOC file
6. ✅ **View note** - Click on uploaded note
7. ✅ **Download** - Download the note
8. ✅ **Comment** - Add a comment
9. ✅ **Admin panel** - Access /admin with superuser credentials

---

## 🐛 **TROUBLESHOOTING**

### **Issue 1: "python is not recognized"**

**Problem:** Python not in PATH

**Solution:**

1. Reinstall Python with "Add to PATH" checked
2. Or manually add Python to PATH:
   - Windows: System Properties → Environment Variables → Path → Add Python folder

### **Issue 2: "No module named 'django'"**

**Problem:** Virtual environment not activated or dependencies not installed

**Solution:**

```bash
# Activate virtual environment first
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Then install dependencies
pip install -r requirements.txt
```

### **Issue 3: "ModuleNotFoundError: No module named 'PIL'"**

**Problem:** Pillow not installed

**Solution:**

```bash
pip install Pillow
```

### **Issue 4: Database errors during migration**

**Problem:** Corrupted database or migration conflict

**Solution:**

```bash
# Delete database and start fresh
del db.sqlite3  # Windows
rm db.sqlite3   # Mac/Linux

# Delete migration files (keep __init__.py)
del notes\migrations\0*.py  # Windows
rm notes/migrations/0*.py   # Mac/Linux

# Re-run migrations
python manage.py makemigrations
python manage.py migrate
```

### **Issue 5: "Port already in use"**

**Problem:** Port 8000 is occupied

**Solution:**

```bash
# Use a different port
python manage.py runserver 8080

# Or kill the process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

### **Issue 6: Static files not loading (no CSS)**

**Problem:** Static files not collected

**Solution:**

```bash
python manage.py collectstatic --noinput
```

### **Issue 7: File upload fails**

**Problem:** Media directory doesn't exist

**Solution:**

```bash
# Windows
mkdir media\notes

# Mac/Linux
mkdir -p media/notes
```

### **Issue 8: PowerShell execution policy error**

**Problem:** Windows blocks running scripts

**Solution:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Issue 9: Virtual environment activation fails**

**Problem:** Activation script not found or permissions

**Solution:**

```bash
# Recreate virtual environment
rmdir venv /s  # Windows
rm -rf venv    # Mac/Linux

python -m venv venv
```

---

## 📁 **PROJECT STRUCTURE**

```
Notes Sharing Platform/
│
├── digital_notes/          # Main project folder
│   ├── __init__.py
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI config
│   └── asgi.py            # ASGI config
│
├── notes/                  # Main app
│   ├── migrations/        # Database migrations
│   ├── management/        # Custom commands
│   │   └── commands/
│   │       └── create_default_admin.py
│   ├── templatetags/      # Custom template filters
│   │   ├── __init__.py
│   │   └── file_helpers.py
│   ├── __init__.py
│   ├── admin.py           # Admin configuration
│   ├── apps.py            # App configuration
│   ├── forms.py           # Django forms
│   ├── models.py          # Database models
│   ├── urls.py            # App URLs
│   ├── views.py           # View functions
│   └── views_setup.py     # Setup view
│
├── templates/              # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── note_list.html
│   ├── note_detail.html
│   ├── upload_note.html
│   └── notes/
│       └── initial_setup.html
│
├── static/                 # Static files
│   └── css/
│       └── style.css
│
├── staticfiles/            # Collected static (auto-generated)
│
├── media/                  # User uploads
│   └── notes/
│
├── venv/                   # Virtual environment (you create this)
│
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── db.sqlite3              # Database (created after migration)
├── setup.bat               # Windows setup script
├── setup.sh                # Linux/Mac setup script
├── create_categories.py    # Category creation script
├── build.sh                # Render deployment script
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── README.md               # Main documentation
├── QUICKSTART.md           # Quick start guide
├── LOCAL_SETUP.md          # This file
├── RENDER_DEPLOYMENT.md    # Render deployment guide
├── RENDER_CHECKLIST.txt    # Deployment checklist
└── ADMIN_CREATION_GUIDE.txt # Admin creation guide
```

---

## 🔄 **DAILY USAGE**

### **Starting the Server:**

**Every time you want to run the project:**

1. **Activate virtual environment:**

   ```bash
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
   ```

2. **Run server:**

   ```bash
   python manage.py runserver
   ```

3. **Access:** http://127.0.0.1:8000/

### **Stopping the Server:**

Press `Ctrl + C` in the terminal.

### **Deactivating Virtual Environment:**

```bash
deactivate
```

---

## 🆘 **COMMON COMMANDS**

```bash
# Activate virtual environment
venv\Scripts\activate              # Windows CMD
venv\Scripts\Activate.ps1          # Windows PowerShell
source venv/bin/activate           # Mac/Linux

# Run development server
python manage.py runserver

# Run on different port
python manage.py runserver 8080

# Create migrations (after model changes)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create default admin (username: admin, password: admin123)
python manage.py create_default_admin

# Create categories
python manage.py shell < create_categories.py

# Collect static files
python manage.py collectstatic

# Open Django shell
python manage.py shell

# Check for issues
python manage.py check

# Install dependencies
pip install -r requirements.txt

# Update dependencies
pip freeze > requirements.txt

# Deactivate virtual environment
deactivate
```

---

## 🎯 **QUICK COMMANDS SUMMARY**

### **First Time Setup:**

```bash
# 1. Clone/copy project
# 2. Open terminal in project directory
# 3. Run ONE of these:

# Windows:
setup.bat

# Mac/Linux:
chmod +x setup.sh && ./setup.sh
```

### **Daily Use:**

```bash
# Activate environment
venv\Scripts\activate  # or source venv/bin/activate

# Run server
python manage.py runserver

# Visit: http://127.0.0.1:8000/
```

---

## 📚 **ADDITIONAL RESOURCES**

- **Django Documentation**: https://docs.djangoproject.com/
- **Python Documentation**: https://docs.python.org/
- **Bootstrap Docs**: https://getbootstrap.com/docs/

---

## ✅ **SUCCESS CHECKLIST**

After setup, verify:

- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (pip list shows Django, Pillow, etc.)
- [ ] Database migrated (db.sqlite3 file exists)
- [ ] Admin user created
- [ ] Categories created (6 categories)
- [ ] Server runs without errors
- [ ] Homepage accessible at http://127.0.0.1:8000/
- [ ] Can register and login
- [ ] Can upload and download notes
- [ ] Admin panel works at /admin

---

## 🎉 **YOU'RE DONE!**

Your Django Notes Sharing Platform is now running locally!

**Default Login (if using create_default_admin):**

- Username: `admin`
- Password: `admin123`

**To share with others:**

- See RENDER_DEPLOYMENT.md for deploying to production
- Free hosting on Render.com

---

**Need help?** Check the troubleshooting section above or the README.md file.
