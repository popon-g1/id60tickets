import os
import datetime
import asyncio
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired, Length
import psycopg2
from psycopg2.extras import RealDictCursor
from telegram import Bot
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Configuration
class Config:
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL')  # Supabase PostgreSQL URL
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')  # Group/channel to send notifications
    
    # Email (optional)
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    NOTIFICATION_EMAIL = os.environ.get('NOTIFICATION_EMAIL')
    
    # Sites configuration
    SITES = {
        "Alkhor": "K",
        "Rayyan": "R", 
        "Mesaimeer": "M",
        "Wakra": "W"
    }

# Database setup
def get_db_connection():
    """Get database connection with error handling"""
    try:
        conn = psycopg2.connect(
            Config.DATABASE_URL,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None

def init_database():
    """Initialize database tables"""
    conn = get_db_connection()
    if not conn:
        logger.error("Cannot initialize database - no connection")
        return False
    
    try:
        cur = conn.cursor()
        
        # Create tickets table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id SERIAL PRIMARY KEY,
                ticket_number VARCHAR(20) UNIQUE NOT NULL,
                site VARCHAR(50) NOT NULL,
                description TEXT NOT NULL,
                status VARCHAR(20) DEFAULT 'Open',
                sender VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index for faster lookups
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_ticket_number ON tickets(ticket_number);
            CREATE INDEX IF NOT EXISTS idx_site ON tickets(site);
            CREATE INDEX IF NOT EXISTS idx_status ON tickets(status);
        """)
        
        conn.commit()
        logger.info("Database initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

# Ticket operations
class TicketManager:
    @staticmethod
    def generate_ticket_number(site: str) -> str:
        """Generate unique ticket number"""
        today_str = datetime.datetime.now().strftime("%Y%m%d")
        site_code = Config.SITES.get(site)
        if not site_code:
            return None
            
        conn = get_db_connection()
        if not conn:
            return None
            
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT COUNT(*) FROM tickets 
                WHERE ticket_number LIKE %s
            """, (f"{today_str}{site_code}%",))
            
            count = cur.fetchone()[0]
            next_number = count + 1
            return f"{today_str}{site_code}{next_number:02d}"
            
        except Exception as e:
            logger.error(f"Error generating ticket number: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def create_ticket(site: str, description: str, sender: str = None) -> Optional[str]:
        """Create new ticket"""
        ticket_number = TicketManager.generate_ticket_number(site)
        if not ticket_number:
            return None
            
        conn = get_db_connection()
        if not conn:
            return None
            
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO tickets (ticket_number, site, description, sender, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (ticket_number, site, description, sender, 'Open'))
            
            conn.commit()
            logger.info(f"Created ticket {ticket_number}")
            return ticket_number
            
        except Exception as e:
            logger.error(f"Error creating ticket: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_all_tickets() -> List[Dict]:
        """Get all tickets"""
        conn = get_db_connection()
        if not conn:
            return []
            
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM tickets 
                ORDER BY created_at DESC
            """)
            return [dict(row) for row in cur.fetchall()]
            
        except Exception as e:
            logger.error(f"Error fetching tickets: {e}")
            return []
        finally:
            conn.close()
    
    @staticmethod
    def get_ticket(ticket_number: str) -> Optional[Dict]:
        """Get specific ticket"""
        conn = get_db_connection()
        if not conn:
            return None
            
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM tickets WHERE ticket_number = %s
            """, (ticket_number,))
            
            row = cur.fetchone()
            return dict(row) if row else None
            
        except Exception as e:
            logger.error(f"Error fetching ticket {ticket_number}: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def update_ticket_status(ticket_number: str, new_status: str) -> bool:
        """Update ticket status"""
        conn = get_db_connection()
        if not conn:
            return False
            
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE tickets 
                SET status = %s, updated_at = CURRENT_TIMESTAMP 
                WHERE ticket_number = %s
            """, (new_status, ticket_number))
            
            if cur.rowcount > 0:
                conn.commit()
                logger.info(f"Updated ticket {ticket_number} to {new_status}")
                return True
            else:
                logger.warning(f"Ticket {ticket_number} not found for update")
                return False
                
        except Exception as e:
            logger.error(f"Error updating ticket {ticket_number}: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

# Notification services
class NotificationService:
    @staticmethod
    async def send_telegram_message(message: str) -> bool:
        """Send message to Telegram"""
        if not Config.TELEGRAM_BOT_TOKEN or not Config.TELEGRAM_CHAT_ID:
            logger.warning("Telegram not configured")
            return False
            
        try:
            bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
            await bot.send_message(
                chat_id=Config.TELEGRAM_CHAT_ID,
                text=message,
                parse_mode='HTML'
            )
            logger.info("Telegram message sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
    
    @staticmethod
    def send_email(subject: str, body: str) -> bool:
        """Send email notification"""
        if not all([Config.EMAIL_USER, Config.EMAIL_PASSWORD, Config.NOTIFICATION_EMAIL]):
            logger.warning("Email not configured")
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = Config.EMAIL_USER
            msg['To'] = Config.NOTIFICATION_EMAIL
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
            server.starttls()
            server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            logger.info("Email sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

# Forms
class TicketForm(FlaskForm):
    site = SelectField('Site', 
                      choices=[(site, site) for site in Config.SITES.keys()],
                      validators=[DataRequired()])
    description = TextAreaField('Description', 
                               validators=[DataRequired(), Length(min=10, max=1000)])
    sender = StringField('Your Name/Contact', 
                        validators=[Length(max=100)])
    submit = SubmitField('Submit Ticket')

class UpdateTicketForm(FlaskForm):
    status = SelectField('Status', 
                        choices=[('Open', 'Open'), ('In Progress', 'In Progress'), 
                                ('Resolved', 'Resolved'), ('Closed', 'Closed')],
                        validators=[DataRequired()])
    submit = SubmitField('Update Status')

# Routes
@app.route('/')
def dashboard():
    """Dashboard with statistics"""
    tickets = TicketManager.get_all_tickets()
    
    # Calculate stats
    total_tickets = len(tickets)
    open_tickets = len([t for t in tickets if t['status'] == 'Open'])
    in_progress_tickets = len([t for t in tickets if t['status'] == 'In Progress'])
    resolved_tickets = len([t for t in tickets if t['status'] == 'Resolved'])
    closed_tickets = len([t for t in tickets if t['status'] == 'Closed'])
    
    # Recent tickets (last 10)
    recent_tickets = tickets[:10]
    
    # Tickets by site
    tickets_by_site = {}
    for site in Config.SITES.keys():
        tickets_by_site[site] = len([t for t in tickets if t['site'] == site])
    
    stats = {
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'in_progress_tickets': in_progress_tickets,
        'resolved_tickets': resolved_tickets,
        'closed_tickets': closed_tickets,
        'tickets_by_site': tickets_by_site
    }
    
    return render_template('dashboard.html', stats=stats, recent_tickets=recent_tickets)

@app.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    """Create new ticket"""
    form = TicketForm()
    
    if form.validate_on_submit():
        ticket_number = TicketManager.create_ticket(
            site=form.site.data,
            description=form.description.data,
            sender=form.sender.data or 'Anonymous'
        )
        
        if ticket_number:
            # Send notifications
            message = f"""
🎫 <b>New Ticket Created</b>

<b>Ticket:</b> {ticket_number}
<b>Site:</b> {form.site.data}
<b>Description:</b> {form.description.data}
<b>Submitted by:</b> {form.sender.data or 'Anonymous'}
<b>Status:</b> Open
            """
            
            # Send Telegram notification (async)
            try:
                asyncio.run(NotificationService.send_telegram_message(message.strip()))
            except Exception as e:
                logger.error(f"Failed to send Telegram notification: {e}")
            
            # Send email notification
            email_subject = f"New IT Support Ticket - {ticket_number}"
            email_body = f"""
            <h2>New IT Support Ticket</h2>
            <p><strong>Ticket Number:</strong> {ticket_number}</p>
            <p><strong>Site:</strong> {form.site.data}</p>
            <p><strong>Description:</strong> {form.description.data}</p>
            <p><strong>Submitted by:</strong> {form.sender.data or 'Anonymous'}</p>
            <p><strong>Status:</strong> Open</p>
            <p><strong>Created:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            """
            
            try:
                NotificationService.send_email(email_subject, email_body)
            except Exception as e:
                logger.error(f"Failed to send email notification: {e}")
            
            flash(f'Ticket {ticket_number} created successfully!', 'success')
            return redirect(url_for('ticket_detail', ticket_number=ticket_number))
        else:
            flash('Failed to create ticket. Please try again.', 'error')
    
    return render_template('create_ticket.html', form=form)

@app.route('/tickets')
def tickets():
    """List all tickets with filtering"""
    site_filter = request.args.get('site', '')
    status_filter = request.args.get('status', '')
    search_query = request.args.get('search', '')
    
    tickets = TicketManager.get_all_tickets()
    
    # Apply filters
    if site_filter and site_filter != 'all':
        tickets = [t for t in tickets if t['site'] == site_filter]
    
    if status_filter and status_filter != 'all':
        tickets = [t for t in tickets if t['status'] == status_filter]
    
    if search_query:
        tickets = [t for t in tickets if 
                  search_query.lower() in t['ticket_number'].lower() or
                  search_query.lower() in t['description'].lower() or
                  search_query.lower() in (t['sender'] or '').lower()]
    
    return render_template('tickets.html', 
                         tickets=tickets,
                         sites=list(Config.SITES.keys()),
                         current_site=site_filter,
                         current_status=status_filter,
                         current_search=search_query)

@app.route('/ticket/<ticket_number>')
def ticket_detail(ticket_number):
    """Ticket detail view"""
    ticket = TicketManager.get_ticket(ticket_number)
    if not ticket:
        flash('Ticket not found.', 'error')
        return redirect(url_for('tickets'))
    
    form = UpdateTicketForm()
    form.status.data = ticket['status']
    
    return render_template('ticket_detail.html', ticket=ticket, form=form)

@app.route('/update_ticket/<ticket_number>', methods=['POST'])
def update_ticket(ticket_number):
    """Update ticket status"""
    form = UpdateTicketForm()
    
    if form.validate_on_submit():
        ticket = TicketManager.get_ticket(ticket_number)
        if not ticket:
            flash('Ticket not found.', 'error')
            return redirect(url_for('tickets'))
        
        old_status = ticket['status']
        new_status = form.status.data
        
        if TicketManager.update_ticket_status(ticket_number, new_status):
            # Send notification about status change
            message = f"""
🔄 <b>Ticket Status Updated</b>

<b>Ticket:</b> {ticket_number}
<b>Site:</b> {ticket['site']}
<b>Status:</b> {old_status} → {new_status}
<b>Updated:</b> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
            """
            
            try:
                asyncio.run(NotificationService.send_telegram_message(message.strip()))
            except Exception as e:
                logger.error(f"Failed to send Telegram notification: {e}")
            
            flash(f'Ticket {ticket_number} updated to {new_status}', 'success')
        else:
            flash('Failed to update ticket.', 'error')
    
    return redirect(url_for('ticket_detail', ticket_number=ticket_number))

@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard stats"""
    tickets = TicketManager.get_all_tickets()
    
    stats = {
        'total_tickets': len(tickets),
        'open_tickets': len([t for t in tickets if t['status'] == 'Open']),
        'in_progress_tickets': len([t for t in tickets if t['status'] == 'In Progress']),
        'resolved_tickets': len([t for t in tickets if t['status'] == 'Resolved']),
        'closed_tickets': len([t for t in tickets if t['status'] == 'Closed']),
    }
    
    return jsonify(stats)

# Initialize database on startup
@app.before_first_request
def initialize():
    init_database()

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Run app
    app.run(host='0.0.0.0', port=5000, debug=True)