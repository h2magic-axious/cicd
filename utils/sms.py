import smtplib

from email.mime.text import MIMEText

from utils.environments import Env


class _SmsSender:
    def __init__(self):
        self.sender = Env.SMS_SENDER
        self.client = smtplib.SMTP(Env.SMTP_SERVER, Env.SMTP_PORT)
        self.client.starttls()
        self.client.login(Env.SMTP_USERNAME, Env.SMTP_PASSWORD)

    def __del__(self):
        self.client.quit()

    def send(self, title: str, text: str, recipient: str):
        message = MIMEText(text)
        message["Subject"] = title
        message["From"] = self.sender
        message["To"] = recipient

        self.client.sendmail(self.sender, recipient, message.as_string())


SmsSender = _SmsSender()
