import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailNotifier:
    @staticmethod
    def send_notification(result):
        sender_email = "your_email@gmail.com"
        receiver_email = "receiver_email@gmail.com"
        password = "your_email_password"

        message = MIMEMultipart("alternative")
        message["Subject"] = "Notificação de Cotas Válidas"
        message["From"] = sender_email
        message["To"] = receiver_email

        text = f"Cotas válidas encontradas: {result}"
        part = MIMEText(text, "plain")
        message.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
