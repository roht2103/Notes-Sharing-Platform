# Digital Notes Sharing Platform

A complete production-ready Django web application for sharing educational notes with clean architecture and best practices.

## 📋 Features

### User Features

- ✅ User Registration & Authentication
- ✅ Upload Notes (PDF, DOC, DOCX only)
- ✅ View & Download Notes
- ✅ Add Comments on Notes
- ✅ Search & Filter Notes by Category
- ✅ Pagination

### Admin Features

- ✅ Manage Users
- ✅ Manage Notes
- ✅ Manage Categories
- ✅ Delete Inappropriate Comments
- ✅ Track Downloads

## 🛠️ Tech Stack

- **Backend:** Django 5.0, Django ORM
- **Database:** SQLite (Development), PostgreSQL Ready (Production)
- **Frontend:** HTML5, Bootstrap 5, CSS3
- **Security:** Django Built-in Authentication, CSRF Protection

## 📁 Project Structure

```
digital_notes/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── digital_notes/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── notes/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── templates/
│   ├── base.html
│   ├── register.html
│   ├── login.html
│   ├── note_list.html
│   ├── upload_note.html
│   └── note_detail.html
│
├── static/
│   └── css/
│       └── style.css
│
└── media/
    └── notes/
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
cd "d:\WORKSPACE\Notes Sharing Platform"
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 6: Create Categories (Important!)

Before users can upload notes, you need to create categories:

**Option 1: Via Django Shell**

```bash
python manage.py shell
```

```python
from notes.models import Category

Category.objects.create(
    category_name="Computer Science",
    description="Notes related to computer science and programming"
)
Category.objects.create(
    category_name="Mathematics",
    description="Mathematical concepts and formulas"
)
Category.objects.create(
    category_name="Science",
    description="Physics, Chemistry, Biology notes"
)
Category.objects.create(
    category_name="Engineering",
    description="Engineering subjects and topics"
)
exit()
```

**Option 2: Via Admin Panel**

1. Run the server: `python manage.py runserver`
2. Go to http://127.0.0.1:8000/admin/
3. Login with superuser credentials
4. Click on "Categories" → "Add Category"
5. Create categories as needed

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

## 🎯 Usage Guide

### For Regular Users

1. **Register an Account**
   - Click "Register" in the navigation bar
   - Fill in the registration form
   - Click "Register" button

2. **Login**
   - Click "Login" in the navigation bar
   - Enter username and password
   - Click "Login" button

3. **Upload a Note**
   - After logging in, click "Upload" in the navigation bar
   - Fill in title, description, select category
   - Choose file (PDF, DOC, or DOCX - max 10MB)
   - Click "Upload Note"

4. **Browse Notes**
   - View all notes on the home page
   - Use search bar to find notes by title
   - Filter by category using dropdown
   - Click "View Details" to see full note information

5. **Download Notes**
   - Click on a note to view details
   - Click "Download Note" button
   - File will be downloaded to your device

6. **Add Comments**
   - On note detail page, scroll to comments section
   - Write your comment in the text area
   - Click "Post Comment"

7. **Delete Your Comments**
   - Only you can delete your own comments
   - Click the trash icon next to your comment

### For Administrators

1. **Access Admin Panel**
   - Go to http://127.0.0.1:8000/admin/
   - Login with superuser credentials

2. **Manage Categories**
   - Add, edit, or delete note categories
   - Update category descriptions

3. **Manage Notes**
   - View all uploaded notes
   - Delete inappropriate notes
   - See download statistics

4. **Manage Users**
   - View all registered users
   - Activate/deactivate user accounts

5. **Moderate Comments**
   - View all comments
   - Delete inappropriate comments
   - Admins can delete any comment

## 🔒 Security Features

- ✅ CSRF Protection on all forms
- ✅ Login Required decorators for protected views
- ✅ File type validation (only PDF, DOC, DOCX)
- ✅ File size limit (10MB max)
- ✅ Password validation
- ✅ SQL Injection prevention (Django ORM)
- ✅ XSS Protection
- ✅ Secure authentication system

## 📊 Database Models

### Category

- category_id (PK)
- category_name (unique)
- description

### Note

- note_id (PK)
- title
- description
- file (FileField)
- uploaded_date
- user_id (FK → User)
- category_id (FK → Category)

### Comment

- comment_id (PK)
- note_id (FK → Note, CASCADE)
- user_id (FK → User, CASCADE)
- content
- comment_date

### Download

- download_id (PK)
- note_id (FK → Note, CASCADE)
- user_id (FK → User, CASCADE)
- download_date
- Unique constraint: (note, user)

## 🌐 URL Routes

| URL                     | View                | Description                     |
| ----------------------- | ------------------- | ------------------------------- |
| `/`                     | note_list           | Home page with all notes        |
| `/register/`            | register_view       | User registration               |
| `/login/`               | login_view          | User login                      |
| `/logout/`              | logout_view         | User logout                     |
| `/upload/`              | upload_note_view    | Upload new note (auth required) |
| `/note/<id>/`           | note_detail_view    | Note details and comments       |
| `/download/<id>/`       | download_note_view  | Download note (auth required)   |
| `/comment/delete/<id>/` | delete_comment_view | Delete comment (auth required)  |
| `/admin/`               | Django Admin        | Admin panel                     |

## 🎨 UI/UX Features

- Responsive Bootstrap 5 design
- Clean and professional interface
- Flash messages for user feedback
- Pagination (9 notes per page)
- Search and filter functionality
- Card-based layout
- Icons from Bootstrap Icons
- Smooth animations and transitions

## 🚀 Production Deployment

### For Production Use:

1. **Update settings.py:**

```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
SECRET_KEY = 'your-secure-secret-key'
```

2. **Configure PostgreSQL:**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'digital_notes_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. **Enable Security Settings:**
   Uncomment security settings in settings.py:

- SECURE_SSL_REDIRECT
- SESSION_COOKIE_SECURE
- CSRF_COOKIE_SECURE
- etc.

4. **Collect Static Files:**

```bash
python manage.py collectstatic
```

5. **Use Production Server:**

- Gunicorn
- uWSGI
- Configure with Nginx/Apache

## 📝 Testing

To test the application:

1. Create superuser and some categories
2. Register a new user account
3. Login with the user account
4. Upload a test note (PDF/DOC/DOCX)
5. View the note on home page
6. Click to view note details
7. Download the note
8. Add a comment
9. Test search and filter functionality
10. Login as admin and test moderation features

## 🐛 Troubleshooting

### Issue: Categories not showing in upload form

**Solution:** Create categories via admin panel or Django shell

### Issue: File upload fails

**Solution:**

- Check file size (must be < 10MB)
- Check file type (must be PDF, DOC, or DOCX)
- Ensure media folder exists and has write permissions

### Issue: Static files not loading

**Solution:**

```bash
python manage.py collectstatic
```

### Issue: Migration errors

**Solution:**

```bash
python manage.py makemigrations notes
python manage.py migrate
```

## 📞 Support

For issues, questions, or contributions, please refer to the project documentation or contact the development team.

## 📄 License

This project is created for educational purposes.

---

**Built with ❤️ using Django**
