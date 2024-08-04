"""Utility functions for the Group Chat application."""

from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime
from email_validator import validate_email, EmailNotValidError


def hash_password(password: str) -> str:
    """
    Hash a password using werkzeug's security functions.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password string
    """
    return generate_password_hash(password, method='pbkdf2:sha256')


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password: Plain text password to verify
        password_hash: Hashed password to check against
        
    Returns:
        True if password matches, False otherwise
    """
    return check_password_hash(password_hash, password)


def validate_username(username: str) -> tuple[bool, str]:
    """
    Validate username format.
    
    Args:
        username: Username to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not username:
        return False, "Username is required"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    
    if len(username) > 20:
        return False, "Username must be at most 20 characters long"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if len(password) > 128:
        return False, "Password is too long"
    
    # Check for at least one letter and one number
    if not re.search(r'[a-zA-Z]', password):
        return False, "Password must contain at least one letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    
    return True, ""


def validate_email_address(email: str) -> tuple[bool, str]:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"
    
    try:
        # Validate and normalize the email address
        valid = validate_email(email)
        return True, ""
    except EmailNotValidError as e:
        return False, str(e)


def sanitize_input(text: str) -> str:
    """
    Sanitize user input by stripping whitespace.
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    return text.strip()


def format_timestamp(timestamp: str) -> str:
    """
    Format a timestamp into a human-readable relative time.
    
    Args:
        timestamp: Timestamp string from database
        
    Returns:
        Formatted time string (e.g., "2 hours ago")
    """
    try:
        # Parse the timestamp (assuming SQLite default format)
        dt = datetime.fromisoformat(timestamp)
        now = datetime.now()
        diff = now - dt
        
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 604800:
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        else:
            # Return formatted date for older posts
            return dt.strftime("%b %d, %Y")
    except (ValueError, AttributeError):
        return timestamp


def validate_group_name(group_name: str) -> tuple[bool, str]:
    """
    Validate group name format.
    
    Args:
        group_name: Group name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not group_name:
        return False, "Group name is required"
    
    if len(group_name) < 3:
        return False, "Group name must be at least 3 characters long"
    
    if len(group_name) > 50:
        return False, "Group name must be at most 50 characters long"
    
    if not re.match(r'^[a-zA-Z0-9_\- ]+$', group_name):
        return False, "Group name can only contain letters, numbers, spaces, hyphens, and underscores"
    
    return True, ""


def validate_post_content(content: str) -> tuple[bool, str]:
    """
    Validate post content.
    
    Args:
        content: Post content to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not content or not content.strip():
        return False, "Post content cannot be empty"
    
    if len(content) > 5000:
        return False, "Post content is too long (maximum 5000 characters)"
    
    return True, ""
