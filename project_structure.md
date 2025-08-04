# 📁 Project Structure

Here's the complete file structure for your IT Support Ticket System:

```
it-support-app/
├── 📄 app.py                    # Main Flask application
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env                      # Environment variables (create from .env.example)
├── 📄 .env.example              # Environment template
├── 📄 wsgi.py                   # PythonAnywhere WSGI config
├── 📄 DEPLOYMENT_GUIDE.md       # Setup instructions
├── 📄 PROJECT_STRUCTURE.md      # This file
├── 📄 README.md                 # Project overview
│
├── 📁 templates/                # HTML templates
│   ├── 📄 base.html             # Base template with navigation
│   ├── 📄 dashboard.html        # Main dashboard page
│   ├── 📄 create_ticket.html    # New ticket form
│   ├── 📄 tickets.html          # All tickets list
│   └── 📄 ticket_detail.html    # Individual ticket view
│
└── 📁 static/ (optional)        # Static files
    ├── 📁 css/
    ├── 📁 js/
    └── 📁 images/
```

## 🔧 Key Files Explained

### Core Application
- **`app.py`** - Main Flask application with all routes and database logic
- **`requirements.txt`** - All Python packages needed
- **`.env`** - Your secret configuration (don't commit to git!)

### Templates
All HTML templates use Bootstrap 5 for responsive design:
- **`base.html`** - Common layout, navigation, and styling
- **`dashboard.html`** - Statistics and recent tickets overview
- **`create_ticket.html`** - Form to submit new support requests
- **`tickets.html`** - Searchable list of all tickets with filters
- **`ticket_detail.html`** - Full ticket view with status updates

### Configuration
- **`.env.example`** - Template showing what environment variables you need
- **`wsgi.py`** - Configuration file for PythonAnywhere deployment

## 🚀 Quick Setup

1. **Create the directory structure** on PythonAnywhere
2. **Upload all files** to their respective folders
3. **Copy `.env.example` to `.env`** and fill in your actual values
4. **Install dependencies** with `pip3.10 install --user -r requirements.txt`
5. **Configure WSGI** file with your username/path
6. **Reload your web app** on PythonAnywhere

## 📋 File Checklist

Before deployment, ensure you have:

- [ ] `app.py` - Main application file
- [ ] `requirements.txt` - Dependencies list
- [ ] `.env` - Your configuration (from .env.example)
- [ ] `wsgi.py` - Updated with your username
- [ ] `templates/base.html` - Base template
- [ ] `templates/dashboard.html` - Dashboard page
- [ ] `templates/create_ticket.html` - New ticket form
- [ ] `templates/tickets.html` - Tickets list
- [ ] `templates/ticket_detail.html` - Ticket details

## 🔄 Development vs Production

### Development (Local)
```bash
# Run locally for testing
python app.py
# Visit http://localhost:5000
```

### Production (PythonAnywhere)
- Files uploaded to `/home/yourusername/it-support-app/`
- WSGI file at `/var/www/yourusername_pythonanywhere_com_wsgi.py`
- Access via `https://yourusername.pythonanywhere.com`

## 💾 Database

The application automatically creates the database schema on first run:
- **`tickets`** table with all necessary columns
- **Indexes** for performance
- **PostgreSQL** (Supabase) or **MySQL** (PythonAnywhere) supported

## 🎨 Customization

### Styling
- Templates use **Bootstrap 5** CDN
- Custom CSS in `<style>` blocks
- Easy to modify colors, layout, branding

### Features
- **Responsive design** - works on mobile/desktop
- **Real-time filtering** - instant search and filters
- **Export functionality** - CSV download
- **Print support** - clean ticket printing

### Adding Features
The modular structure makes it easy to add:
- User authentication
- File attachments
- Comments/updates
- Email templates
- Admin panel