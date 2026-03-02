"""
Quick script to create sample categories
Run with: python manage.py shell < create_categories.py
"""
from notes.models import Category

categories = [
    {
        'category_name': 'Computer Science',
        'description': 'Programming, Data Structures, Algorithms, Software Engineering'
    },
    {
        'category_name': 'Mathematics',
        'description': 'Calculus, Linear Algebra, Statistics, Discrete Mathematics'
    },
    {
        'category_name': 'Science',
        'description': 'Physics, Chemistry, Biology, Environmental Science'
    },
    {
        'category_name': 'Engineering',
        'description': 'Mechanical, Electrical, Civil, Chemical Engineering'
    },
    {
        'category_name': 'Business',
        'description': 'Management, Marketing, Finance, Economics'
    },
    {
        'category_name': 'Arts & Humanities',
        'description': 'Literature, History, Philosophy, Languages'
    },
]

print("Creating categories...")
created_count = 0

for cat_data in categories:
    category, created = Category.objects.get_or_create(
        category_name=cat_data['category_name'],
        defaults={'description': cat_data['description']}
    )
    if created:
        created_count += 1
        print(f"✓ Created: {category.category_name}")
    else:
        print(f"- Already exists: {category.category_name}")

print(f"\nTotal categories created: {created_count}")
print(f"Total categories in database: {Category.objects.count()}")
