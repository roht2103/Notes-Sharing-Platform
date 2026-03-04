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

# Optional: Create default admin user (comment out for security in production)
# python manage.py create_default_admin

echo "Build completed successfully!"
