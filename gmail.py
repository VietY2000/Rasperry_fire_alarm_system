import smtplib, ssl
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import  MIMEMultipart
from email.mime.base import MIMEBase
class email():
    def send_mail(img_source,email):
        subject = "Fire! Fire! Fire!"
        body = "Fire image"
        sender_email = "*****@gmail.com"
        receiver_email = email
        password = "*****" # password email provide for python

        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        message.attach(MIMEText(body))

        file_name = img_source

        with open(file_name, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header("Content-Disposition", f"attachment; filename= {file_name}",
                        )
        message.attach(part)
        text = message.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email,receiver_email, text)

if __name__ == "__main__":
    email.send_mail("img_sourc","*****@gmail.com")