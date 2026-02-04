import pika
import sys
import os
import json
import time
from minio import Minio
from io import BytesIO


RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = 'user'
RABBITMQ_PASS = 'password'

MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'minio:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin')
BUCKET_NAME = "incident-logs"

def get_minio_client():
    return Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )

def upload_to_minio(payload):
    try:
        client = get_minio_client()
        if not client.bucket_exists(BUCKET_NAME):
            client.make_bucket(BUCKET_NAME)
            print(f"Bucket '{BUCKET_NAME}' created.")

        data = json.dumps(payload, indent=2).encode('utf-8')
        data_stream = BytesIO(data)
        filename = f"incident_{int(time.time())}.json"
        
        client.put_object(
            BUCKET_NAME,
            filename,
            data_stream,
            length=len(data),
            content_type='application/json'
        )
        print(f"Saved report to Minio: {filename}")
        
    except Exception as e:
        print(f"Minio Error: {e}")

def callback(ch, method, properties, body):
    print(f"Received Alert: {body}")
    try:
        payload = json.loads(body)
        upload_to_minio(payload)
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    print(f"Connecting to RabbitMQ at {RABBITMQ_HOST} as {RABBITMQ_USER}...")
    
    # Credentials
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    
    connection = None
    while connection is None:
        try:
            connection = pika.BlockingConnection(parameters)
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ auth failed or not ready, retrying in 5s")
            time.sleep(5)

    channel = connection.channel()
    channel.queue_declare(queue='critical_incidents', durable=True)

    print('Waiting for messages.')
    channel.basic_consume(queue='critical_incidents', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass