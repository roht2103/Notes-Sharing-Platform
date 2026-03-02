# PythonAnywhere Deployment Guide
## Digital Notes Sharing Platform

Complete step-by-step guide to deploy your Django application on PythonAnywhere.

---

## 📋 **Pre-Deployment Checklist**

Before deploying, you need:
- ✅ A PythonAnywhere account (free tier works fine)
- ✅ Your Django project files
- ✅ GitHub account (recommended for easy upload)

---

## 🚀 **STEP 1: Create PythonAnywhere Account**

1. Go to [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Click **"Pricing & signup"**
3. Choose **"Create a Beginner account"** (FREE)
4. Complete registration
5. Verify your email

**Free Tier Includes**:
- One web app at `yourusername.pythonanywhere.com`
- 512 MB storage
- Limited CPU time

---

## 🚀 **STEP 2: Upload Your Project**

### **Option A: Using GitHub (Recommended)**

1. **Create GitHub Repository**
   ```bash
   # On your local machine
   cd "D:\WORKSPACE\Notes Sharing Platform"
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   ```

2. **Create repo on GitHub.com**
   - Go to github.com → New Repository
   - Name: `notes-sharing-platform`
   - Click "Create repository"

3. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/notes-sharing-platform.git
   git push -u origin main
   ```

4. **Clone on PythonAnywhere**
   - Login to PythonAnywhere
   - Go to **"Consoles"** tab → Start new **"Bash"** console
   ```bash
   cd ~
   git clone https://github.com/YOUR_USERNAME/notes-sharing-platform.git
   cd notes-sharing-platform
   ```

### **Option B: Manual Upload (Slower)**

1. Login to PythonAnywhere
2. Go to **"Files"** tab
3. Create directory: `notes-sharing-platform`
4. Upload all files manually (NOT recommended for large projects)

---

## 🚀 **STEP 3: Set Up Virtual Environment**

In PythonAnywhere Bash console:

```bash
# Navigate to project directory
cd ~/notes-sharing-platform

# Create virtual environment with Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 notesenv

# Activate virtual environment
workon notesenv

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

**Expected output**: Django 5.0.x, Pillow 10.x installed

---

## 🚀 **STEP 4: Configure Django Settings**

### **4.1: Update ALLOWED_HOSTS**

Edit `digital_notes/settings.py`:

```python
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'localhost', '127.0.0.1']
```

Replace `yourusername` with your actual PythonAnywhere username.

### **4.2: Set DEBUG to False (for production)**

```python
DEBUG = False
```

⚠️ **Important**: Keep `DEBUG = True` during initial setup to see errors, then change to `False` once working.

---

## 🚀 **STEP 5: Set Up Database**

In PythonAnywhere Bash console:

```bash
cd ~/notes-sharing-platform
workon notesenv

# Run migrations
python manage.py migrate

# Create categories
python manage.py shell
```

In the Python shell:
```python
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

exit()
```

**Create admin user**:
```bash
python manage.py create_default_admin
# This creates: username=admin, password=admin123
```

Or create custom admin:
```bash
python manage.py createsuperuser
# Follow prompts to create your admin account
```

---

## 🚀 **STEP 6: Collect Static Files**

```bash
cd ~/notes-sharing-platform
workon notesenv
python manage.py collectstatic --noinput
```

This copies all CSS, JS, images to `/static/` directory.

---

## 🚀 **STEP 7: Configure Web App on PythonAnywhere**

### **7.1: Create Web App**

1. Go to **"Web"** tab
2. Click **"Add a new web app"**
3. Choose your domain: `yourusername.pythonanywhere.com`
4. Select **"Manual configuration"**
5. Choose **"Python 3.10"**

### **7.2: Configure Virtual Environment**

In the **Web** tab, scroll to **"Virtualenv"** section:

```
/home/yourusername/.virtualenvs/notesenv
```

Replace `yourusername` with your actual username.

### **7.3: Configure WSGI File**

1. In the **Web** tab, click on **WSGI configuration file** link
   (e.g., `/var/www/yourusername_pythonanywhere_com_wsgi.py`)

2. **Delete all contents** and replace with:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/notes-sharing-platform'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'digital_notes.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**⚠️ Replace `yourusername`** with your PythonAnywhere username in line 5!

3. Click **"Save"** (top right)

---

## 🚀 **STEP 8: Configure Static Files**

In the **Web** tab, scroll to **"Static files"** section:

Add these two mappings:

| URL           | Directory                                          |
|---------------|---------------------------------------------------|
| `/static/`    | `/home/yourusername/notes-sharing-platform/static` |
| `/media/`     | `/home/yourusername/notes-sharing-platform/media`  |

**⚠️ Replace `yourusername`** with your actual username!

Click the **green checkmarks** to save.

---

## 🚀 **STEP 9: Reload Web App**

1. Go to top of **Web** tab
2. Click the big green **"Reload yourusername.pythonanywhere.com"** button
3. Wait for reload to complete (takes 10-20 seconds)

---

## 🚀 **STEP 10: Test Your Application**

1. Click on your domain link: `https://yourusername.pythonanywhere.com`
2. You should see your Notes Sharing Platform!

### **Test These Features**:
- ✅ Home page loads with notes list
- ✅ Register new account
- ✅ Login with new account
- ✅ Upload a note (PDF/DOC)
- ✅ View note details
- ✅ Download note
- ✅ Add comment
- ✅ Admin panel: `yourusername.pythonanywhere.com/admin`
  - Login: `admin` / `admin123`

---

## 🐛 **Troubleshooting Common Issues**

### **Issue 1: "ImportError: No module named 'digital_notes'"**

**Solution**:
- Check WSGI file has correct path
- Verify virtual environment is set correctly
- Reload web app

### **Issue 2: "DisallowedHost" Error**

**Solution**:
Edit `settings.py`:
```python
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
```
Then reload web app.

### **Issue 3: Static Files Not Loading (No CSS)**

**Solution**:
1. Run `python manage.py collectstatic`
2. Check Static files mappings in Web tab
3. Reload web app

### **Issue 4: "OperationalError: database is locked"**

**Solution**:
- This happens with SQLite under load
- For production, consider PostgreSQL
- For now, just reload the page

### **Issue 5: File Upload Fails**

**Solution**:
```bash
cd ~/notes-sharing-platform
mkdir -p media/notes
chmod 755 media
chmod 755 media/notes
```

### **View Error Logs**

If something goes wrong:
1. Go to **Web** tab
2. Scroll to **"Log files"** section
3. Click **"Error log"** to see detailed errors

---

## 🔒 **Security Improvements (Optional)**

### **1. Change Secret Key**

Edit `settings.py`:
```python
import os
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-new-secret-key-here')
```

Generate new secret key:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### **2. Change Default Admin Password**

```bash
cd ~/notes-sharing-platform
workon notesenv
python manage.py changepassword admin
```

### **3. Set Up Environment Variables**

In PythonAnywhere Bash:
```bash
echo 'export SECRET_KEY="your-secret-key"' >> ~/.bashrc
source ~/.bashrc
```

---

## 📝 **Update/Deploy Changes**

When you make changes to your code:

### **If using GitHub**:
```bash
# On your local machine
git add .
git commit -m "Your changes"
git push

# On PythonAnywhere Bash console
cd ~/notes-sharing-platform
git pull
workon notesenv
python manage.py migrate  # If models changed
python manage.py collectstatic --noinput  # If static files changed
# Then reload web app from Web tab
```

### **If uploading manually**:
1. Upload changed files via Files tab
2. Reload web app from Web tab

---

## 📊 **Monitoring**

### **Check Logs**:
- Go to **Web** tab
- Check **Error log** for Python errors
- Check **Server log** for HTTP requests
- Check **Access log** for traffic

### **Usage Limits**:
- Go to **Account** tab
- Monitor CPU usage
- Free tier: 100 CPU-seconds/day

---

## 🎉 **Success!**

Your Django Notes Sharing Platform is now live at:
**`https://yourusername.pythonanywhere.com`**

Share this URL with others to let them use your platform!

---

## 📚 **Next Steps**

1. ✅ Change default admin password
2. ✅ Set DEBUG = False in production
3. ✅ Upload some sample notes
4. ✅ Test all features
5. ✅ Share your platform URL!

---

## 🆘 **Need Help?**

- PythonAnywhere Forums: [www.pythonanywhere.com/forums/](https://www.pythonanywhere.com/forums/)
- PythonAnywhere Help: [help.pythonanywhere.com](https://help.pythonanywhere.com)
- Django Docs: [docs.djangoproject.com](https://docs.djangoproject.com)

---

**Deployment Date**: {{ current_date }}  
**Django Version**: 5.0.14  
**Python Version**: 3.10  
**Platform**: PythonAnywhere
