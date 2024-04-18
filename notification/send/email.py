import json
import smtplib
import os
import logging

from email.message import EmailMessage


# Method receives as argument the RabbitMQ queue read message
def notification(message):
    try:
        message = json.loads(message)
        logging.info(f"Loaded RabbitMQ message into JSON: {message}")
        mp3_fid = message['mp3_fid']
        # For demonstration purposes, using Google's SMTP server for sending emails. Will use dummy account.
        sender_address = os.environ.get("EMAIL_ADDRESS")
        sender_password = os.environ.get("EMAIL_PASSWORD")
        recipient_address = message['username']

        # Prepare Email message details
        logging.info("Preparing email with queue message information ...")
        msg = EmailMessage()
        msg.set_content(f'mp3 file_id: {mp3_fid} is now ready')
        msg["Subject"] = "MP3 Download"
        msg["From"] = sender_address
        msg["To"] = recipient_address

        # Create SMTP Server session for sending the email
        session = smtplib.SMTP("smtp.office365.com")
        session.starttls()
        session.login(sender_address, sender_password)
        session.send_message(msg, sender_address, recipient_address)
        session.quit()
        logging.info("Email notification sent to user")

    except Exception as ex:
        logging.error("Error occurred while processing the RabbitMQ message or sending an email notification")
        logging.error(f"Exception: {ex}")
        # Returns the exception as the call to this function expects it
        return ex

