import os
import pandas as pd
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

load_dotenv()

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_LOG_FILE = "emails.csv"

# Create the emails.csv if it doesn't exist
if not os.path.exists(EMAIL_LOG_FILE):
    pd.DataFrame(columns=["timestamp", "email"]).to_csv(EMAIL_LOG_FILE, index=False)

def log_email(email: str):
    email_entry = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "email": email
    }])
    email_entry.to_csv(EMAIL_LOG_FILE, mode='a', header=False, index=False)

def send_followup_email(recipient_email: str) -> bool:
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = "Thanks for chatting with us!"

        body = """\
Hi there,

Thank you for your time! If you have any further questions, feel free to reply to this email.
We look forward to continuing our conversation.

Best regards,  
Sales Team
"""
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email send failed: {e}")
        return False
