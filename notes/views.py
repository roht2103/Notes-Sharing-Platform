from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from .models import Note, Comment, Download
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    NoteUploadForm,
    CommentForm,
    NoteSearchForm
)


def register_view(request):
    """
    Handle user registration
    """
    if request.user.is_authenticated:
        return redirect('note_list')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """
    Handle user login
    Redirect admin users to admin panel, normal users to note list
    """
    if request.user.is_authenticated:
        # Redirect authenticated users based on their role
        if request.user.is_staff:
            return redirect('/admin/')
        return redirect('note_list')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Redirect based on user role
                if user.is_staff or user.is_superuser:
                    messages.success(request, f'Welcome Admin, {username}!')
                    return redirect('/admin/')
                else:
                    messages.success(request, f'Welcome back, {username}!')
                    next_url = request.GET.get('next', 'note_list')
                    return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def logout_view(request):
    """
    Handle user logout
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


def note_list_view(request):
    """
    Display list of all notes with search and filter functionality
    Includes pagination
    """
    notes = Note.objects.select_related('user', 'category').annotate(
        download_count=Count('downloads')
    )
    
    # Handle search and filter
    search_form = NoteSearchForm(request.GET)
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        category = search_form.cleaned_data.get('category')
        
        if search_query:
            notes = notes.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if category:
            notes = notes.filter(category=category)
    
    # Pagination - 9 notes per page
    paginator = Paginator(notes, 9)
    page = request.GET.get('page')
    
    try:
        notes_page = paginator.page(page)
    except PageNotAnInteger:
        notes_page = paginator.page(1)
    except EmptyPage:
        notes_page = paginator.page(paginator.num_pages)
    
    context = {
        'notes': notes_page,
        'search_form': search_form,
        'total_notes': notes.count()
    }
    
    return render(request, 'note_list.html', context)


@login_required(login_url='login')
def upload_note_view(request):
    """
    Handle note upload
    Only authenticated users can upload notes
    """
    if request.method == 'POST':
        form = NoteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, 'Note uploaded successfully!')
            return redirect('note_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NoteUploadForm()
    
    return render(request, 'upload_note.html', {'form': form})


def note_detail_view(request, pk):
    """
    Display detailed view of a note with comments
    Handle comment submission
    """
    note = get_object_or_404(
        Note.objects.select_related('user', 'category'),
        pk=pk
    )
    comments = note.comments.select_related('user').all()
    
    # Check if current user has downloaded this note
    has_downloaded = False
    if request.user.is_authenticated:
        has_downloaded = note.is_downloaded_by_user(request.user)
    
    # Handle comment form submission
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to comment.')
            return redirect('login')
        
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.note = note
            comment.user = request.user
            comment.addComment()
            messages.success(request, 'Comment added successfully!')
            return redirect('note_detail', pk=pk)
    else:
        comment_form = CommentForm()
    
    context = {
        'note': note,
        'comments': comments,
        'comment_form': comment_form,
        'download_count': note.get_download_count(),
        'has_downloaded': has_downloaded
    }
    
    return render(request, 'note_detail.html', context)


@login_required(login_url='login')
def download_note_view(request, pk):
    """
    Handle note download
    Create download record and serve file
    """
    note = get_object_or_404(Note, pk=pk)
    
    try:
        # Try to create download record (will fail if already downloaded due to unique_together)
        download = Download(note=note, user=request.user)
        download.recordDownload()
    except Exception:
        # User has already downloaded this note
        pass
    
    try:
        # Serve the file
        file_handle = note.file.open('rb')
        response = FileResponse(file_handle, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{note.file.name.split("/")[-1]}"'
        messages.success(request, f'Downloading: {note.title}')
        return response
    except Exception:
        messages.error(request, 'Error downloading file. Please try again.')
        return redirect('note_detail', pk=pk)


@login_required(login_url='login')
def delete_comment_view(request, pk):
    """
    Delete a comment
    Only the comment owner or admin can delete
    """
    comment = get_object_or_404(Comment, pk=pk)
    note_id = comment.note.note_id
    
    if comment.can_delete(request.user):
        comment.deleteComment()
        messages.success(request, 'Comment deleted successfully!')
    else:
        messages.error(request, 'You do not have permission to delete this comment.')
    
    return redirect('note_detail', pk=note_id)
