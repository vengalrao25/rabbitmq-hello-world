# RabbitMQ Hello World (Python)

A simple producer and consumer for RabbitMQ. It uses the `pika` library.

## How it works

```
send.py  --->  default exchange ('')  --->  queue "hello"  --->  receive.py
```

- `send.py` (producer): connects to RabbitMQ, declares the `hello` queue, and sends one message.
- `receive.py` (consumer): connects to RabbitMQ, declares the same queue, and prints each message it gets.
- The queue is a **durable quorum queue**. It stays after a broker restart.
- The message goes through the **default exchange** (`''`). This exchange sends a message to the queue with the same name as the routing key (`hello`).
- Both scripts declare the queue. Thus you can start them in any order.
- The consumer uses `auto_ack=True`. RabbitMQ removes the message when it sends it to the consumer.

## Requirements

- Python 3
- RabbitMQ on `localhost`, port `5673`

To start RabbitMQ with Docker:

```bash
docker run -d --name rabbitmq -p 5673:5672 -p 15672:15672 rabbitmq:3-management
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

Terminal 1 (consumer):

```bash
python receive.py
```

Terminal 2 (producer):

```bash
python send.py
```

The consumer shows ` [x] Received ...`. Press `CTRL+C` to stop it.
