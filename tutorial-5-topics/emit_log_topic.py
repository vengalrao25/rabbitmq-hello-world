#!/usr/bin/env python
import pika
import sys

# Connect to the RabbitMQ broker on this machine
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5673))
channel = connection.channel()

# Topic exchange: matches the routing key against the binding patterns
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# ROUTING KEY = exact words split by "." (no "*" or "#" here)
# Example: python emit_log_topic.py "kern.critical" "Disk full"
#   -> routing_key = 'kern.critical', message = 'Disk full'
# With no arguments, the routing key is 'anonymous.info'
routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(
    exchange='topic_logs', routing_key=routing_key, body=message)
print(f" [x] Sent {routing_key}:{message}")
connection.close()
