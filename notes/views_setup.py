"""
One-time setup view to create admin user via web interface
This is an alternative to using Shell on Render free tier
"""
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import os


@require_http_methods(["GET", "POST"])
def initial_setup(request):
    """
    One-time setup page to create the first admin user.
    Disabled after first admin is created or if DISABLE_SETUP is set.
    """
    # Check if setup is disabled
    if os.environ.get('DISABLE_SETUP', 'False') == 'True':
        messages.error(request, 'Setup has been disabled.')
        return redirect('note_list')

    # Check if any superuser exists
    if User.objects.filter(is_superuser=True).exists():
        messages.warning(request, 'Admin user already exists. Setup is complete.')
        return redirect('login')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        # Validation
        errors = []
        if not username:
            errors.append('Username is required.')
        if not email:
            errors.append('Email is required.')
        if not password:
            errors.append('Password is required.')
        if password != password_confirm:
            errors.append('Passwords do not match.')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters.')
        if User.objects.filter(username=username).exists():
            errors.append('Username already exists.')

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Create superuser
            try:
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    first_name='Admin',
                    last_name='User'
                )
                messages.success(
                    request,
                    f'Admin user "{username}" created successfully! You can now login.'
                )
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error creating admin user: {str(e)}')

    return render(request, 'notes/initial_setup.html')
