import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_email(receiver_email,subject,body,attachment=None,filename=None,subtype=None):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'ponrajiitm@gmail.com'
    app_password = 'zlbw qcrk qgac ilud'  # Use the app password here

    # Create the email
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Email body
    message.attach(MIMEText(body, "html"))
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        server.login(sender_email, app_password)  # Log in with the app password
        if attachment:
            part = MIMEApplication(attachment.read(), _subtype=subtype)
            part.add_header("Content-Disposition", "attachment", filename= filename)
            message.attach(part)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
        print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')
    finally:
        server.quit()  # Close the connection