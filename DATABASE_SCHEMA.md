# Database Schema Documentation

## Overview
This document describes the database schema for the Group Chat application.

## Tables

### 1. user
Stores user account information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique user identifier |
| username | TEXT | UNIQUE NOT NULL | User's login username |
| password | TEXT | NOT NULL | Hashed password |

### 2. userinfo
Stores additional user profile information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| user_id | INTEGER | PRIMARY KEY, FK(user.id) | References user table |
| firstname | TEXT | NOT NULL | User's first name |
| middlename | TEXT | | User's middle name (optional) |
| lastname | TEXT | NOT NULL | User's last name |
| email | TEXT | UNIQUE NOT NULL | User's email address |
| dob | TEXT | NOT NULL | Date of birth |
| gender | TEXT | NOT NULL | User's gender |

### 3. user_group
Stores group/community information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique group identifier |
| name | TEXT | UNIQUE NOT NULL | Group name |

### 4. group_member
Junction table for user-group relationships (many-to-many).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| user_id | INTEGER | FK(user.id), PRIMARY KEY | User ID |
| group_id | INTEGER | FK(user_group.id), PRIMARY KEY | Group ID |

**Composite Primary Key**: (user_id, group_id)

### 5. posts
Stores posts made in groups.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique post identifier |
| content | TEXT | NOT NULL | Post content |
| user_id | INTEGER | FK(user.id) NOT NULL | Author of the post |
| group_id | INTEGER | FK(user_group.id) NOT NULL | Group where post was made |
| doc | DATE | DEFAULT CURRENT_DATE | Date of creation |

### 6. comment
Stores comments on posts.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique comment identifier |
| comment | TEXT | NOT NULL | Comment content |
| post_id | INTEGER | FK(posts.id) NOT NULL | Post being commented on |
| user_id | INTEGER | FK(user.id) NOT NULL | Author of the comment |
| commented_on | DATE | DEFAULT CURRENT_DATE | Date of comment |

### 7. like
Stores likes on posts (many-to-many relationship).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| post_id | INTEGER | FK(posts.id), PRIMARY KEY | Post being liked |
| user_id | INTEGER | FK(user.id), PRIMARY KEY | User who liked |

**Composite Primary Key**: (post_id, user_id)

## Entity Relationships

```
user (1) ----< (N) userinfo
user (1) ----< (N) group_member >----< (N) user_group
user (1) ----< (N) posts >---- (1) user_group
user (1) ----< (N) comment >---- (1) posts
user (1) ----< (N) like >----< (N) posts
```

## Key Design Decisions

1. **user_group table**: Stores group information with just `id` and `name` columns for simplicity
2. **group_member table**: Junction table enabling many-to-many relationship between users and groups
3. **Composite primary keys**: Used in junction tables (`group_member`, `like`) to ensure uniqueness
4. **Foreign key constraints**: Maintain referential integrity across all relationships
5. **Date fields**: Use `DATE DEFAULT CURRENT_DATE` for automatic timestamp creation
