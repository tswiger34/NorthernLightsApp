from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel
from typing import List
import os

class EmailSchema(BaseModel):
    email: str
    subject: str
    message: str

class NotificationManager:
    def __init__(self):
        self.mail_config = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
            MAIL_FROM=os.getenv("MAIL_FROM"),
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_TLS=True,
            MAIL_SSL=False,
            USE_CREDENTIALS=True,
        )
        self.fast_mail = FastMail(self.mail_config)

    async def send_notification(self, email: EmailSchema):
        message = MessageSchema(
            subject=email.subject,
            recipients=[email.email],
            body=email.message,
            subtype="html"
        )
        await self.fast_mail.send_message(message)

    def notify_users(self, emails: List[EmailSchema], background_tasks: BackgroundTasks):
        for email in emails:
            background_tasks.add_task(self.send_notification, email)