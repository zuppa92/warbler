# Warbler Project Changes

## Overview
This document outlines the changes made to the Warbler project, including bug fixes, new features, and improvements.

## Changes Log

### 1. Initial Setup
- **Installed Dependencies:**
  - Resolved issues with dependencies in `requirements.txt`.
  - Updated `requirements.txt` to compatible versions:
    - `Flask==2.0.3`
    - `Flask-Bcrypt==1.0.1`
    - `Flask-DebugToolbar==0.11.1`
    - `Flask-SQLAlchemy==2.5.1`
    - `Flask-WTF==0.15.1`
    - `psycopg2-binary==2.9.6`
    - `Werkzeug==2.0.3`
    - `WTForms==3.0.1`

### 2. Fixing Import Errors
- **Updated Imports in `models.py`:**
  - Fixed import errors related to `collections` module by replacing deprecated `MutableMapping` with `collections.abc.MutableMapping`.
  - Fixed import errors related to `url_encode` by replacing it with `urllib.parse.quote`.

### 3. Database Setup
- **Database Configuration:**
  - Created the database `warbler` using `psql` commands.
  - Ran `seed.py` to populate the database with initial data.

### 4. Implementing Logout Functionality
- **Added Logout Route:**
  - Created a `/logout` route in `app.py` to handle user logout.
  - On logout, the session is cleared, a success message is flashed, and the user is redirected to the login page.

### 5. Flash Messages
- **Added Flash Messages to Base Template:**
  - Updated `base.html` to include flash message display logic.
  - Ensured flash messages are styled appropriately using Bootstrap alert classes.

### 6. Debugging and Testing
- **Debugging Tools:**
  - Set up `pdb` for debugging routes and models.
  - Verified relationships in models using interactive debugger.

### 7. Fix User Profile
- **Updated User Profile Page:**
  - Updated the user profile page (`profile.html`) to include:
    - User location
    - User bio
    - User header image (displayed as a background at the top)
- **Updated `app.py` for Profile Edits:**
  - Updated the `/users/profile` route to handle profile edits:
    - Users can now update their location, bio, and header image URL.
  - Added validation for the updated fields in the `UserEditForm` in `forms.py`.

### 8. Updated `forms.py`
- **Added `UserEditForm`:**
  - Added the `UserEditForm` class with the following fields:
    - `username`: String field for the user's username (required)
    - `email`: String field for the user's email (required)
    - `image_url`: String field for the user's image URL (optional)
    - `header_image_url`: String field for the user's header image URL (optional)
    - `bio`: Text area field for the user's bio (optional)
    - `location`: String field for the user's location (optional)
    - `password`: Password field for the user's password (required for verification)

### 9. Template Changes
- **Updated `profile.html`:**
  - Display the user's location and bio.
  - Use the header image as a background at the top of the profile page.
  - Added an edit profile button if the logged-in user is viewing their own profile.

### 10. Fix User Cards
- **Updated User Cards:**
  - On the followers, following, and list-users pages, updated the user cards to show the bio for the users.

### 11. Profile Edit Implementation
- **Implemented Profile Edit:**
  - Added buttons throughout the site for editing the profile.
  - Ensured a user is logged in to access the edit profile form.
  - Included the following fields in the edit profile form:
    - username
    - email
    - image_url
    - header_image_url
    - bio
    - location
    - password (for verification)
  - Checked that the password is the valid password for the user before allowing updates.
  - Redirected to the user detail page on successful profile update.

### 12. Add Likes Functionality
- **Implemented Likes Feature:**
  - Users can now like and unlike warbles (messages) posted by other users.
  - Added a star icon next to liked warbles.
  - Displayed the number of likes a user has
