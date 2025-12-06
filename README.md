# Notes App

A modern, mobile-first Django web application for creating, managing, and sharing personal notes with social features.

## Features

- **User Authentication**: Email-based registration and login with custom user profiles
- **Note Management**: Create, edit, delete, and organize personal notes
- **Public/Private Notes**: Share notes publicly or keep them private
- **Comments System**: Add comments to public notes for collaboration
- **Social Features**: Follow other users and view their public notes
- **Profile Management**: Custom profile pictures, bios, and user slugs
- **Responsive Design**: Mobile-optimized interface with PWA capabilities
- **Image Processing**: Automatic profile picture resizing and optimization

## Tech Stack

- **Backend**: Django 5.1.7
- **Database**: SQLite (development), PostgreSQL (production recommended)
- **Frontend**: HTML5, CSS3, Bootstrap
- **Image Processing**: Django ImageKit, Pillow
- **PWA Features**: Service Worker, Web App Manifest

## Installation

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd notes-app
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your browser and go to `http://127.0.0.1:8000`

## Usage

### User Registration and Login

- Visit the home page and click "Sign Up" to create a new account
- Use your email address for authentication
- Complete your profile with a picture and bio

### Creating Notes

- Log in to your account
- Click "Add Note" to create a new note
- Choose whether to make it public or private
- Use the rich text editor to format your content

### Managing Notes

- View all your notes on the dashboard
- Edit or delete notes using the action buttons
- Toggle visibility between public and private

### Social Features

- Browse public notes from all users on the home page
- Follow other users to see their updates
- Comment on public notes to engage with content

### Mobile App

The application is PWA-enabled. On mobile devices, you can:
- Add to home screen for app-like experience
- Use offline capabilities (limited)
- Receive push notifications (future feature)

## Project Structure

```
notes-app/
├── accounts/              # User authentication and profiles
├── notes/                 # Note and comment models/views
├── website/               # Static pages and PWA features
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── media/                 # User-uploaded files
├── django_project/        # Django settings and URLs
└── manage.py             # Django management script
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please open an issue on GitHub or contact the development team.
