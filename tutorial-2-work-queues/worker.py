#!/usr/bin/env python
import pika
import time

# Connect to the RabbitMQ broker on this machine
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5673))
channel = connection.channel()

# Make sure the "task_queue" queue exists (same settings as new_task.py)
channel.queue_declare(queue='task_queue', durable=True, arguments={'x-queue-type': 'quorum'})
print(' [*] Waiting for messages. To exit press CTRL+C')


# Do the "work" (sleep 1 second per "."), then ack so the broker deletes the message
def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Give this worker only 1 unacked message at a time (fair dispatch)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
