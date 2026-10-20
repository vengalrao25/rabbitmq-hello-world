#!/usr/bin/env python
import pika
import sys

# Connect to the RabbitMQ broker on this machine
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5673))
channel = connection.channel()

# Make sure the "task_queue" queue exists (durable quorum queue)
channel.queue_declare(queue='task_queue', durable=True, arguments={'x-queue-type': 'quorum'})

# Each "." in the message means 1 second of work for the worker
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent
    ))
print(f" [x] Sent {message}")
connection.close()
