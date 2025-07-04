# ServiceConnect - Worker Service Platform

## Overview

ServiceConnect is a Flask-based web application that connects daily workers (plumbers, electricians, carpenters, cleaners, etc.) with customers seeking local services. The platform allows workers to register their services and customers to find and contact service professionals in their area.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 dark theme
- **Responsive Design**: Mobile-first approach using Bootstrap grid system
- **JavaScript**: Vanilla JavaScript for interactive features (image preview, search functionality)
- **Styling**: Custom CSS combined with Bootstrap and Font Awesome icons

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Form Handling**: Flask-WTF for form validation and CSRF protection
- **File Uploads**: Werkzeug secure filename handling for profile images
- **Session Management**: Flask sessions with configurable secret key

### Data Storage
- **Primary Storage**: JSON file-based storage (`data/workers.json`)
- **File Storage**: Local filesystem for uploaded profile images (`static/uploads/`)
- **No Database**: Simple file-based approach for lightweight deployment

## Key Components

### Core Application Files
- **app.py**: Main Flask application with routes and business logic
- **forms.py**: WTForms classes for worker registration and contact forms
- **main.py**: Application entry point for deployment

### Templates
- **base.html**: Base template with navigation and layout structure
- **index.html**: Homepage with hero section and service categories
- **workers.html**: Worker listing page with search and filter functionality
- **register.html**: Worker registration form
- **worker_profile.html**: Individual worker profile pages
- **contact.html**: Contact form page

### Static Assets
- **CSS**: Custom styling in `static/css/style.css`
- **JavaScript**: Interactive features in `static/js/main.js`
- **Uploads**: Profile images stored in `static/uploads/`

## Data Flow

1. **Worker Registration**: Workers fill out registration form → Data validation → Profile image upload → JSON storage
2. **Worker Discovery**: Customers browse/search workers → Filter by service/location → View detailed profiles
3. **Contact Process**: Customers contact workers through contact form → Email notification (future feature)

## External Dependencies

### Python Packages
- **Flask**: Web framework
- **Flask-WTF**: Form handling and CSRF protection
- **WTForms**: Form validation
- **Werkzeug**: File upload security

### Frontend Libraries
- **Bootstrap 5**: UI framework with dark theme
- **Font Awesome**: Icon library
- **Replit Bootstrap Theme**: Custom dark theme integration

### File Upload Configuration
- **Allowed Extensions**: PNG, JPG, JPEG, GIF
- **Max File Size**: 16MB
- **Upload Directory**: `static/uploads/`

## Deployment Strategy

### Development Setup
- **Debug Mode**: Enabled for development
- **Host**: 0.0.0.0 (all interfaces)
- **Port**: 5000
- **Environment Variables**: Session secret key

### Production Considerations
- File-based storage suitable for small to medium scale
- Static file serving handled by Flask (consider CDN for production)
- Session secret should be set via environment variable

### Scalability Limitations
- JSON file storage not suitable for high-traffic applications
- No user authentication system implemented
- No database relationships or complex queries

## Changelog
- July 04, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.