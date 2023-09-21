import smtplib
from email.mime.text import MIMEText
import os
from log_config import logger

MY_EMAIL = os.environ.get('MY_EMAIL')
APP_PASSWORD = os.environ.get('APP_PASSWORD')


def send_exchange_rate_email(exchange_rate: float) -> bool:
    destination_email = os.environ.get('DEST_EMAIL')

    # Create the message content
    subject = f"AUD exchange rate for today."
    body_content = (f"Hey Visa Clerk\n\nThe Exchange rate for today is: {exchange_rate}."
                    f"\n\nIt has been updated in the database. Verify that this is correct.")

    # Create MIMEText object
    msg = MIMEText(body_content)
    msg['Subject'] = subject
    msg['From'] = MY_EMAIL
    msg['To'] = destination_email
    done_or_not = None
    try:
        # Use context manager for SMTP to ensure the connection is automatically closed
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(MY_EMAIL, APP_PASSWORD)
            server.sendmail(MY_EMAIL, destination_email, msg.as_string())
        done_or_not = True
    except Exception as e:
        logger.error(f"An error occurred while sending the email. The error is {str(e)}")
        done_or_not = False
    finally:
        email_sent = done_or_not

    return email_sent
