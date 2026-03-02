#!/bin/bash
# ============================================================
# PythonAnywhere Setup Script
# Run this in PythonAnywhere Bash console after uploading code
# ============================================================

echo "╔══════════════════════════════════════════════════════╗"
echo "║  Digital Notes Platform - PythonAnywhere Setup      ║"
echo "╚══════════════════════════════════════════════════════╝"

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Are you in the project directory?"
    echo "Run: cd ~/notes-sharing-platform"
    exit 1
fi

echo ""
echo "📦 Step 1: Creating virtual environment..."
mkvirtualenv --python=/usr/bin/python3.10 notesenv
workon notesenv

echo ""
echo "📦 Step 2: Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "🗄️  Step 3: Setting up database..."
python manage.py migrate

echo ""
echo "📂 Step 4: Creating categories..."
python manage.py shell << EOF
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
    obj, created = Category.objects.get_or_create(**cat)
    if created:
        print(f"✅ Created: {obj.category_name}")
    else:
        print(f"⏭️  Already exists: {obj.category_name}")
EOF

echo ""
echo "👤 Step 5: Creating admin user..."
python manage.py create_default_admin

echo ""
echo "📁 Step 6: Creating media directories..."
mkdir -p media/notes
chmod 755 media
chmod 755 media/notes

echo ""
echo "🎨 Step 7: Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  ✅ Setup Complete!                                  ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "📝 Next Steps:"
echo "1. Go to PythonAnywhere Web tab"
echo "2. Configure WSGI file (see pythonanywhere_wsgi.py)"
echo "3. Set up static files mappings"
echo "4. Reload your web app"
echo ""
echo "🔐 Default Admin Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo "   ⚠️  CHANGE THIS AFTER FIRST LOGIN!"
echo ""
echo "🌐 Your site will be at:"
echo "   https://YOUR_USERNAME.pythonanywhere.com"
echo ""
