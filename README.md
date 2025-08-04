# 🎫 IT Support Ticket System

A modern, responsive web application for managing IT support tickets with real-time notifications via Telegram and email.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3+-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-orange)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)

## ✨ Features

### 🎯 Core Functionality
- **Create Tickets** - Simple form-based ticket submission
- **Track Status** - Open → In Progress → Resolved → Closed workflow
- **Search & Filter** - Find tickets by site, status, or keywords
- **Dashboard** - Real-time statistics and recent activity
- **Responsive Design** - Works on desktop, tablet, and mobile

### 🔔 Notifications
- **Telegram Integration** - Instant notifications to groups/channels
- **Email Alerts** - HTML formatted email notifications
- **Real-time Updates** - Status changes trigger automatic notifications

### 🏢 Multi-Site Support
- **Site Management** - Support for multiple locations (Alkhor, Rayyan, Mesaimeer, Wakra)
- **Site-specific Filtering** - View tickets by location
- **Unique Ticket Numbers** - Auto-generated with site codes (e.g., 20240804K01)

### 📊 Reporting & Analytics
- **Dashboard Statistics** - Ticket counts by status and site
- **Export Functionality** - Download tickets as CSV
- **Print Support** - Clean ticket printing
- **Recent Activity** - Track latest ticket updates

## 🏗️ Architecture

### Technology Stack
- **Backend**: Python 3.10+ with Flask framework
- **Database**: PostgreSQL (Supabase) with automatic schema creation
- **Frontend**: Bootstrap 5, vanilla JavaScript
- **Notifications**: Telegram Bot API, SMTP email
- **Deployment**: PythonAnywhere (free tier compatible)

### Design Principles
- **Clean Architecture** - Separation of concerns with dedicated classes
- **Mobile-First** - Responsive design that works everywhere
- **Zero-Config** - Automatic database initialization
- **Production Ready** - Proper error handling and logging

## 🚀 Quick Start

### 1. Clone or Download
```bash
# Create your project directory
mkdir it-support-app
cd it-support-app
```

### 2. Set Up Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration:
# - Database URL (Supabase PostgreSQL)
# - Telegram bot token and chat ID
# - Email credentials (optional)
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Locally
```bash
python app.py
# Visit http://localhost:5000
```

### 5. Deploy to PythonAnywhere
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 📱 Usage Guide

### Creating a Ticket
1. Navigate to **"New Ticket"**
2. Select the affected **site**
3. Enter a detailed **description**
4. Add your **name/contact** (optional)
5. Click **"Submit Ticket"**

### Managing Tickets
1. View all tickets in **"All Tickets"**
2. Use **filters** to find specific tickets
3. Click **ticket number** for full details
4. Update **status** as work progresses
5. Use **quick actions** for common updates

### Dashboard Overview
- **Statistics** - Total, open, in-progress, resolved, closed tickets
- **Recent Activity** - Latest 10 tickets with quick access
- **Site Breakdown** - Visual representation of tickets by location
- **Quick Actions** - One-click access to common tasks

## 🔧 Configuration

### Required Environment Variables
```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host:5432/db
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=-1001234567890
```

### Optional Email Configuration
```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
NOTIFICATION_EMAIL=notifications@company.com
```

### Site Configuration
Edit the `SITES` dictionary in `app.py` to match your locations:
```python
SITES = {
    "Location1": "L1",
    "Location2": "L2",
    # Add your sites here
}
```

## 🔔 Notification Setup

### Telegram Bot
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Create new bot: `/newbot`
3. Get your bot token
4. Add bot to your group/channel
5. Get chat ID from `https://api.telegram.org/bot[TOKEN]/getUpdates`

### Email Notifications
1. Use Gmail app passwords (not regular password)
2. Enable 2FA on your Google account
3. Generate app-specific password
4. Use this password in `EMAIL_PASSWORD`

## 📊 Database Schema

The application automatically creates this schema:

```sql
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    ticket_number VARCHAR(20) UNIQUE NOT NULL,
    site VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'Open',
    sender VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🎨 Customization

### Styling
- Built with **Bootstrap 5** for easy customization
- Custom CSS classes for status badges and cards
- Print-friendly styles included

### Adding Features
The modular architecture makes it easy to add:
- **User Authentication** - Login/logout system
- **File Attachments** - Upload screenshots or documents
- **Comments** - Add updates and notes to tickets
- **Categories** - Organize tickets by type
- **Priority Levels** - Urgent, high, medium, low
- **Assignment** - Assign tickets to specific technicians

### Extending Notifications
- **Slack Integration** - Send to Slack channels
- **SMS Notifications** - Via Twilio or similar
- **Push Notifications** - Browser notifications
- **Webhook Support** - Integrate with other systems

## 🔒 Security Features

- **CSRF Protection** - Form security with Flask-WTF
- **SQL Injection Prevention** - Parameterized queries
- **Environment Variables** - Secrets not in code
- **Input Validation** - Form validation and sanitization
- **Secure Headers** - Standard security headers

## 📈 Performance

### Optimization Features
- **Database Indexes** - Fast ticket lookups
- **Lazy Loading** - Efficient data fetching  
- **Caching Headers** - Browser caching for static assets
- **Minimal Dependencies** - Fast startup and low memory

### Scaling Considerations
- **Connection Pooling** - For high-traffic deployments
- **Redis Cache** - For session and query caching
- **Load Balancing** - Multiple app instances
- **CDN Integration** - For static asset delivery

## 🐛 Troubleshooting

### Common Issues

**Database Connection Failed**
- Verify `DATABASE_URL` format
- Check Supabase project status
- Confirm firewall/network access

**Telegram Not Working**
- Validate bot token format
- Ensure chat ID is correct (negative for groups)
- Check bot permissions in group

**Email Issues**
- Use app passwords, not regular passwords
- Verify SMTP settings
- Check spam folders

**Template Errors**
- Ensure all template files exist
- Check file permissions
- Verify directory structure

## 📞 Support

### Getting Help
1. Check the [Deployment Guide](DEPLOYMENT_GUIDE.md)
2. Review [Project Structure](PROJECT_STRUCTURE.md)
3. Search existing issues
4. Create detailed bug reports

### Contributing
We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Flask** - Lightweight and powerful web framework
- **Bootstrap** - Beautiful, responsive UI components  
- **Supabase** - Excellent PostgreSQL hosting
- **PythonAnywhere** - Easy Python web app deployment
- **Telegram** - Reliable messaging platform for notifications

---

**Made with ❤️ for IT support teams everywhere**
