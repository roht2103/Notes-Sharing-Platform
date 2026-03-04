"""
Template tags for safe file operations
"""
from django import template
import os

register = template.Library()


@register.filter(name='file_exists')
def file_exists(file_field):
    """
    Check if a file exists on the filesystem
    Usage: {% if note.file|file_exists %}
    """
    if not file_field:
        return False
    try:
        return file_field.storage.exists(file_field.name)
    except Exception:
        return False


@register.filter(name='safe_file_size')
def safe_file_size(file_field):
    """
    Safely get file size, return 0 if file doesn't exist
    Usage: {{ note.file|safe_file_size|filesizeformat }}
    """
    if not file_field:
        return 0
    try:
        if file_field.storage.exists(file_field.name):
            return file_field.size
        return 0
    except Exception:
        return 0
