# main.py
import os
import smtplib
from email.mime.text import MIMEText
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

class EmailRequest(BaseModel):
    email: EmailStr

@app.post("/send-email")
async def send_email(data: EmailRequest):
    # Compose the message
    msg = MIMEText("Hello! 👋 This is a test message from FastAPI.")
    msg["Subject"] = "Hello from FastAPI"
    msg["From"] = os.environ["GMAIL_USER"]
    msg["To"] = data.email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(os.environ["GMAIL_USER"], os.environ["GMAIL_PASS"])
            server.send_message(msg)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Email failed to send")

    return {"ok": True, "message": f"Hello email sent to {data.email}"}
