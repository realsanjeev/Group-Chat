"""Flask-WTF forms for the Group Chat application."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import re


class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"),
        Length(min=3, max=20, message="Username must be between 3 and 20 characters")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required")
    ])


class SignupForm(FlaskForm):
    """Form for user registration."""
    firstname = StringField('First Name', validators=[
        DataRequired(message="First name is required"),
        Length(max=50, message="First name is too long")
    ])
    middlename = StringField('Middle Name', validators=[
        Length(max=50, message="Middle name is too long")
    ])
    lastname = StringField('Last Name', validators=[
        DataRequired(message="Last name is required"),
        Length(max=50, message="Last name is too long")
    ])
    gender = RadioField('Gender', choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], validators=[DataRequired(message="Please select a gender")])
    dob = DateField('Date of Birth', validators=[
        DataRequired(message="Date of birth is required")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address")
    ])
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"),
        Length(min=3, max=20, message="Username must be between 3 and 20 characters")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    password_repeat = PasswordField('Repeat Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('password', message="Passwords must match")
    ])
    
    def validate_username(self, field):
        """Validate username format."""
        if not re.match(r'^[a-zA-Z0-9_]+$', field.data):
            raise ValidationError("Username can only contain letters, numbers, and underscores")
    
    def validate_password(self, field):
        """Validate password strength."""
        password = field.data
        if not re.search(r'[a-zA-Z]', password):
            raise ValidationError("Password must contain at least one letter")
        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one number")


class CreateGroupForm(FlaskForm):
    """Form for creating a new group."""
    group_name = StringField('Group Name', validators=[
        DataRequired(message="Group name is required"),
        Length(min=3, max=50, message="Group name must be between 3 and 50 characters")
    ])
    
    def validate_group_name(self, field):
        """Validate group name format."""
        if not re.match(r'^[a-zA-Z0-9_\- ]+$', field.data):
            raise ValidationError("Group name can only contain letters, numbers, spaces, hyphens, and underscores")


class JoinGroupForm(FlaskForm):
    """Form for joining an existing group."""
    group_name = StringField('Group Name', validators=[
        DataRequired(message="Group name is required"),
        Length(min=3, max=50, message="Group name must be between 3 and 50 characters")
    ])


class CreatePostForm(FlaskForm):
    """Form for creating a new post."""
    content = TextAreaField('Post Content', validators=[
        DataRequired(message="Post content cannot be empty"),
        Length(max=5000, message="Post content is too long (maximum 5000 characters)")
    ])
