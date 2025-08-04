# IT Support Ticket System - Deployment Guide

## 🚀 Quick Start

This guide will help you deploy your Flask IT Support Ticket System on PythonAnywhere with PostgreSQL (Supabase) integration.

## 📋 Prerequisites

- [PythonAnywhere](https://www.pythonanywhere.com/) free account
- [Supabase](https://supabase.com/) account (PostgreSQL database)
- [Telegram Bot](https://t.me/BotFather) token
- Gmail account for email notifications (optional)

## 🗄️ Database Setup (Supabase)

1. **Create Supabase Project**
   - Go to [Supabase](https://supabase.com/)
   - Create new project
   - Wait for provisioning to complete

2. **Get Database Connection String**
   - Go to Settings → Database
   - Copy the connection string
   - Format: `postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres`

3. **Database will be auto-initialized** when the app first runs

## 🤖 Telegram Bot Setup

1. **Create Bot**
   ```
   Message @BotFather on Telegram:
   /newbot
   Choose a name: IT Support Bot
   Choose username: your_support_bot
   ```

2. **Get Bot Token**
   - Copy the token (format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

3. **Get Chat ID**
   - Add bot to your group/channel
   - Send a test message
   - Visit: `https://api.telegram.org/bot[YOUR-BOT-TOKEN]/getUpdates`
   - Find the chat ID in the response

## 🐍 PythonAnywhere Deployment

### Step 1: Upload Files

1. **Login to PythonAnywhere**
   - Go to Files → Upload files

2. **Create Project Structure**
   ```
   /home/yourusername/
   ├── it-support-app/
   │   ├── app.py
   │   ├── requirements.txt
   │   ├── .env
   │   └── templates/
   │       ├── base.html
   │       ├── dashboard.html
   │       ├── create_ticket.html
   │       ├── tickets.html
   │       └── ticket_detail.html
   ```

### Step 2: Environment Configuration

1. **Create `.env` file**
   ```bash
   SECRET_KEY=your-super-secret-key-here
   DATABASE_URL=postgresql://postgres:yourpassword@db.yourproject.supabase.co:5432/postgres
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_CHAT_ID=-1001234567890
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   NOTIFICATION_EMAIL=notifications@yourcompany.com
   ```

### Step 3: Install Dependencies

1. **Open Bash Console**
   ```bash
   cd ~/it-support-app
   pip3.10 install --user -r requirements.txt
   ```

### Step 4: Web App Configuration

1. **Go to Web tab**
2. **Create new web app**
   - Python 3.10
   - Manual configuration

3. **Configure WSGI file**
   - Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`
   - Replace content with the provided `wsgi.py` code
   - Update the path to your project directory

4. **Set Static Files** (optional)
   - URL: `/static/`
   - Directory: `/home/yourusername/it-support-app/static/`

### Step 5: Test & Launch

1. **Initialize Database**
   ```bash
   cd ~/it-support-app
   python3.10 app.py
   # Ctrl+C to stop after database is initialized
   ```

2. **Reload Web App**
   - Go to Web tab
   - Click "Reload yourusername.pythonanywhere.com"

3. **Test the Application**
   - Visit your app URL
   - Create a test ticket
   - Verify Telegram notifications work

## 🔧 Configuration Details

### Telegram Integration
- Sends notifications for new tickets
- Sends updates when ticket status changes
- Messages include ticket details and status

### Email Notifications (Optional)
- Gmail SMTP configuration
- App passwords required (not regular password)
- HTML formatted emails

### Database Schema
The app automatically creates these tables:
- `tickets` - Main ticket storage
- Indexes for performance optimization

## 📱 Usage

### Creating Tickets
1. Go to "New Ticket"
2. Select site
3. Enter description
4. Submit

### Managing Tickets
1. View all tickets in "All Tickets"
2. Filter by site, status, or search
3. Click ticket number for details
4. Update status as needed

### Status Flow
- **Open** → In Progress → Resolved → Closed
- Tickets can be reopened if needed

## 🔒 Security Notes

- Change the `SECRET_KEY` in production
- Use environment variables for all sensitive data
- Database connections are encrypted (Supabase)
- Form validation and CSRF protection included

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check DATABASE_URL format
   - Verify Supabase project is active
   - Check firewall/network settings

2. **Telegram Not Working**
   - Verify bot token is correct
   - Check chat ID format (should start with -)
   - Ensure bot is added to the group

3. **Import Errors**
   - Run: `pip3.10 install --user -r requirements.txt`
   - Check Python version compatibility

4. **Template Not Found**
   - Verify templates/ directory structure
   - Check file permissions

### Logs
- Check PythonAnywhere error logs in Web tab
- Add logging to your code for debugging

## 🔄 Updates & Maintenance

### Updating the Application
1. Upload new files
2. Reload web app
3. Test functionality

### Database Backups
- Supabase provides automatic backups
- Export data regularly for local backups

### Monitoring
- Check logs regularly
- Monitor Telegram bot status
- Verify email deliverability

## 💡 Next Steps

After deployment, consider:
- Adding user authentication
- Implementing file uploads
- Adding email templates
- Creating admin dashboard
- Setting up monitoring/alerts

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review PythonAnywhere logs
3. Test components individually
4. Verify all environment variables are set correctly