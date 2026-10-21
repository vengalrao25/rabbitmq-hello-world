#!/usr/bin/env python
import pika
import sys

# Connect to the RabbitMQ broker on this machine
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5673))
channel = connection.channel()

# Fanout exchange: sends a copy of each message to all bound queues
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Fanout ignores the routing key, so we leave it empty
message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs', routing_key='', body=message)
print(f" [x] Sent {message}")
connection.close()
