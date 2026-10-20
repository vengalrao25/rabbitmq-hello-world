#!/usr/bin/env python
import pika

# Connect to the RabbitMQ broker on this machine
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5673))
channel = connection.channel()

# Make sure the "hello" queue exists (same settings as send.py)
channel.queue_declare(queue='hello', durable=True, arguments={'x-queue-type': 'quorum'})


# Called each time a message arrives
def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")


# Read messages from "hello" and auto-acknowledge them
channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
