from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import os


def validate_file_size(file):
    """Validate that uploaded file is not larger than 10MB"""
    max_size_mb = 10
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'File size cannot exceed {max_size_mb}MB')


class Category(models.Model):
    """Model for note categories"""
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['category_name']

    def __str__(self):
        return self.category_name

    def addCategory(self):
        """Method to add a category"""
        self.save()

    def deleteCategory(self):
        """Method to delete a category"""
        self.delete()


class Note(models.Model):
    """Model for notes uploaded by users"""
    note_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(
        upload_to='notes/',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']),
            validate_file_size
        ]
    )
    uploaded_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='notes')

    class Meta:
        ordering = ['-uploaded_date']
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'

    def __str__(self):
        return self.title

    def get_download_count(self):
        """Get the number of times this note has been downloaded"""
        return self.downloads.count()

    def is_downloaded_by_user(self, user):
        """Check if a specific user has downloaded this note"""
        return self.downloads.filter(user=user).exists()
    
    @property
    def filename(self):
        """Get just the filename without path"""
        return os.path.basename(self.file.name)
    
    @property
    def file_extension(self):
        """Get the file extension"""
        return os.path.splitext(self.file.name)[1].lstrip('.').upper()


class Comment(models.Model):
    """Model for comments on notes"""
    comment_id = models.AutoField(primary_key=True)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_date']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'Comment by {self.user.username} on {self.note.title}'

    def addComment(self):
        """Method to add a comment"""
        self.save()

    def deleteComment(self):
        """Method to delete a comment"""
        self.delete()

    def can_delete(self, user):
        """Check if a user can delete this comment (admin or comment owner)"""
        return user.is_staff or user == self.user


class Download(models.Model):
    """Model to track note downloads"""
    download_id = models.AutoField(primary_key=True)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='downloads')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downloads')
    download_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-download_date']
        verbose_name = 'Download'
        verbose_name_plural = 'Downloads'
        # Prevent duplicate download records per user per note (optional bonus feature)
        unique_together = ['note', 'user']

    def __str__(self):
        return f'{self.user.username} downloaded {self.note.title}'

    def recordDownload(self):
        """Method to record a download"""
        self.save()
