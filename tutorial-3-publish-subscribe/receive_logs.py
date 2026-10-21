#!/usr/bin/env python
import pika

# Connect to the RabbitMQ broker on this machine
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5673))
channel = connection.channel()

# Make sure the "logs" exchange exists (same settings as emit_log.py)
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# queue='' = the broker makes a random queue name (amq.gen-...)
# exclusive=True = the broker deletes the queue when this connection closes
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Bind our queue to the "logs" exchange, so it gets a copy of each message
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {body}")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
