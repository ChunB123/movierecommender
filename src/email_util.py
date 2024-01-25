import smtplib
from email.message import EmailMessage

def send_email(content):
    sender_email = "franktiger98@outlook.com"
    sender_password = ""
    receiver_email = "jiazheng.xu@mail.mcgill.ca"
    # receiver_email = "chengzhiyin98@gmail.com"

    # Create the email message
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = 'COMP585 Project'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send the email via Outlook's SMTP server
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp:
        smtp.starttls()  # Start TLS encryption
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

    print("Email sent successfully!")

# Example usage
# send_email("Hello, this is a test email.")
