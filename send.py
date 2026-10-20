#!/usr/bin/env python
import pika

# Connect to the RabbitMQ broker on this machine
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5673))
channel = connection.channel()

# Make sure the "hello" queue exists (durable quorum queue)
channel.queue_declare(queue='hello', durable=True, arguments={'x-queue-type': 'quorum'})

# Send through the default exchange ('') straight to the "hello" queue
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='new World!')
print(" [x] Sent 'Hello World!'")

# Close the connection so the message is flushed to the broker
connection.close()
