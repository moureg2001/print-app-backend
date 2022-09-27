import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ServiceController.service_controller import ServiceBaseController
from .config import config


class EmailSender(ServiceBaseController):
    def __init__(self, subject=None, body=None, filename=None):
        self.subject = subject
        self.body = body
        self.filename = filename
        self.message = MIMEMultipart()
        self.text = ""
        self.__email_init__()

    def __email_init__(self):
        # Create a multipart message and set headers
        # message = MIMEMultipart()
        self.message["From"] = config['sender_email']
        self.message["To"] = config['receiver_email']
        self.message["Subject"] = self.subject
        self.message["Bcc"] = config['receiver_email']  # Recommended for mass emails
        # Add body to email
        self.message.attach(MIMEText(self.body, "plain"))

    def add_attachment(self, filename):
        # filename = "keychain.stl"  # In same directory as script
        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            # Add attachment to message and convert message to string
            self.message.attach(part)
            self.text = self.message.as_string()

    def login_send_email(self):
        print("...Sending an Email...")
        # Log in to server using secure context and send email
        # context = ssl.create_default_context()
        # Try to log in to server and send email
        try:
            with smtplib.SMTP(config['smtp_ssl'], config['port']) as server:
                server.login(config['email_user'], config['email_password'])
                self.add_attachment(config['file_path'])
                print(f"Text: {self.text}")
                server.sendmail(config['sender_email'], config['receiver_email'], self.text)
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        # finally:
        # server.quit()

# mailer = EmailSender("This is the second test e-mail message", "Die stl Datei ist Druck Bereit!",
#                      "../EmailService/ATTACHMENT/keychain.stl")
# mailer.login_send_email()
