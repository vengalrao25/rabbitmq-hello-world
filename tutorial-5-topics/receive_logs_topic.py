#!/usr/bin/env python
import pika
import sys

# Connect to the RabbitMQ broker on this machine
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5673))
channel = connection.channel()

# Make sure the "topic_logs" exchange exists (same settings as emit_log_topic.py)
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# Server-named, exclusive queue only for this consumer
result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

# Binding keys are PATTERNS. The "*" and "#" are written here, not in the producer.
#   "*" = exactly 1 word, "#" = 0 or more words
# Example: python receive_logs_topic.py "kern.*" "*.critical"
#   -> binding_keys = ['kern.*', '*.critical']
binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

# One binding for each pattern.
# In queue_bind, pika calls it "routing_key", but it is the BINDING KEY (the pattern).
for binding_key in binding_keys:
    channel.queue_bind(
        exchange='topic_logs', queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
