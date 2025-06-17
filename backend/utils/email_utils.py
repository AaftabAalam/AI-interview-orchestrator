import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your-email@example.com'
SENDER_PASSWORD = 'your-email-password'

def send_email(to_address: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg['FROM'] = SENDER_EMAIL
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_address, msg.as_string())
    except Exception as e:
        print(f"Failed to send email to {to_address}: {e}")

def send_interview_invitation(candidate_email: str, candidate_name: str, scheduled_time: str, duration: int, link: str):
    subject = "Your Interview Is Scheduled"
    body = (
        f"Dear {candidate_name},\n\n"
        f"Your interview has been scheduled for {scheduled_time}.\n"
        f"Duration: {duration} minutes\n"
        f"Interview link: {link}\n\n"
        f"Please be available at the scheduled time.\n\n"
        f"Best regards,\nThe Interview Team"
    )

    send_email(candidate_email, subject, body)

def notify_host_of_scheduled_interview(host_email: str, candidate_name: str, candidate_email: str, scheduled_time: str):
    subject = "New Interview Scheduled"
    body = (
        f"A new candidate has been scheduled with the following details:\n\n"
        f"Candidate name: {candidate_name}\n"
        f"Candidate email: {candidate_email}\n"
        f"Scheduled Time: {scheduled_time}\n\n"
    )
    send_email(host_email, subject, body)

def send_reschedule_notification(candidate_email: str, candidate_name: str, new_time: str, link: str):
    subject = "Interview Rescheduled"
    body = (
        f"Dear {candidate_name},\n\n"
        f"Your interview has been rescheduled to {new_time}.\n"
        f"Interview Link: {link}\n\n"
    )
    send_email(candidate_email, subject, body)

def notify_host_of_rescheduled_interview(host_email: str, candidate_name: str, candidate_email: str, new_time: str):
    subject = "Interview Rescheduled"
    body = (
        f"The following interview has been rescheduled:\n\n"
        f"Candidate name: {candidate_name}\n"
        f"Candidate email: {candidate_email}\n"
        f"New scheduled time: {new_time}\n\n"
    )

    send_email(host_email, subject, body)
    