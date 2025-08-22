import smtplib
from kafka import KafkaConsumer
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()
sender = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

receiver = os.getenv("RECEIVER")

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(sender,password)

consumer = KafkaConsumer(
    'postgres.public.totals',
    bootstrap_servers = 'kafka:29092',
    auto_offset_reset = 'earliest',
    enable_auto_commit = True,
    group_id = 'totals-trigger',
    value_deserializer = lambda x: json.loads(x.decode('utf-8')) if x else None
)

print("Connected to kakfa topic that tracks totals table for low stock alert")

for message in consumer:
    data = message.value
    if not data or 'after' not in data:
        continue
    
    after = data['after']
    if not after or 'total' not in after:
        continue

    total = after['total']
    product_id = after['product_id']
    
    if total <= 10:
        subject = f"Low stock alert for {product_id}"
        body = f"Product {product_id} has low stock : {total}"
        email_message = f"{subject}\n\n{body}"
        server.sendmail(sender,receiver,email_message)