from flask import Flask, jsonify
from azure.storage.blob import BlobServiceClient
from azure.communication.email import EmailClient
from dotenv import load_dotenv
import os
import asyncio
import atexit
import smtplib
from email.mime.text import MIMEText
from threading import Thread
import time

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

print(os.getenv("EMAIL_URL"))

# Azure Blob Storage configuration
account_name = os.getenv("STORAGE_ACCOUNT_NAME")
account_key = os.getenv("STORAGE_ACCOUNT_KEY")
container_name = "lab9"
blob_service_client = BlobServiceClient(
    account_url=f"https://{account_name}.blob.core.windows.net",
    credential=account_key
)

# Azure Communication Email configuration
email_connection_string = os.getenv("EMAIL_URL")
email_client = EmailClient.from_connection_string(email_connection_string)
# email_client = EmailClient(email_connection_string)

# Email sending function
async def send_email(address, count):
    message = {
        "senderAddress": "DoNotReply@4904e9fc-529c-44b9-a650-b0247c395169.azurecomm.net",
        "recipients":  {
            "to": [{"address": "prasadsb240801@gmail.com" }],
        },
        "content": {
            "subject": "Test Email",
            "plainText": "Hello world via email.",
        }
    }

    poller = await email_client.begin_send(email_message)
    result = await poller.poll_until_done()
    print("Result:", result)

# Initialize blob count
initial_count = 0

async def fetch_blobs():
    container_client = blob_service_client.get_container_client(container_name)
    blobs = container_client.list_blobs()
    blob_names = [blob.name for blob in blobs]
    return blob_names

def check_blob_count():
    global initial_count
    while True:
        current_blobs = asyncio.run(fetch_blobs())
        current_count = len(current_blobs)
        if current_count != initial_count:
            print("Blob count has changed. Sending notification...")
            asyncio.run(send_email("jaidevv999@gmail.com", current_count))
            initial_count = current_count
        else:
            print("No change in blob count.")
        time.sleep(2)

@app.route('/')
def index():
    blobs = asyncio.run(fetch_blobs())
    return jsonify({"result": blobs})

if __name__ == '__main__':
    # Start background thread for checking blob count
    thread = Thread(target=check_blob_count)
    thread.daemon = True
    thread.start()
    app.run(port=int(os.getenv("PORT", 8888)))
