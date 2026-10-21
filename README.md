# RabbitMQ Tutorials (Python)

RabbitMQ tutorials in Python. They use the `pika` library.

| Folder | Tutorial |
| --- | --- |
| `tutorial-1-hello-world/` | Hello World |
| `tutorial-2-work-queues/` | Work Queues |
| `tutorial-3-publish-subscribe/` | Publish/Subscribe |

## Tutorial 1: Hello World

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

## Run tutorial 1

Terminal 1 (consumer):

```bash
python tutorial-1-hello-world/receive.py
```

Terminal 2 (producer):

```bash
python tutorial-1-hello-world/send.py
```

The consumer shows ` [x] Received ...`. Press `CTRL+C` to stop it.

## Tutorial 2: Work Queues

```
new_task.py  --->  queue "task_queue"  --->  worker.py (1)
                                       --->  worker.py (2)
```

- `new_task.py` (producer): sends one task. Each `.` in the message means 1 second of work.
- `worker.py` (consumer): does the task, then sends an ack.
- **Round-robin:** RabbitMQ gives each task to one worker only. More workers do more tasks at the same time.
- **Manual ack:** the worker sends the ack after the work is done. If a worker stops before the ack, RabbitMQ sends the task to a different worker.
- **Fair dispatch:** `prefetch_count=1` gives a worker a new task only after it sends the ack for its last task.
- **Durable:** `task_queue` is a quorum queue, so the tasks stay after a broker restart.

## Run tutorial 2

Terminal 1 and terminal 2 (workers):

```bash
python tutorial-2-work-queues/worker.py
```

Terminal 3 (producer):

```bash
python tutorial-2-work-queues/new_task.py "First task."
python tutorial-2-work-queues/new_task.py "Second task.."
python tutorial-2-work-queues/new_task.py "Third task..."
```

To see the redelivery, stop a worker with `CTRL+C` while it works on a task. The other worker gets that task.

## Tutorial 3: Publish/Subscribe

```
emit_log.py --> exchange "logs" (fanout) --> amq.gen-A (exclusive) --> receive_logs.py (1)
                                         --> amq.gen-B (exclusive) --> receive_logs.py (2)
```

- `emit_log.py` (producer): publishes to the `logs` fanout exchange, not to a queue.
- `receive_logs.py` (consumer): declares its own server-named, exclusive queue and binds it to `logs`.
- **Fanout:** the exchange sends a copy of each message to all bound queues. It ignores the routing key.
- **Server-named queue:** `queue=''` makes the broker create a random name (`amq.gen-...`). The consumer reads it from `result.method.queue`.
- **Exclusive:** the broker deletes the queue when the consumer connection closes.
- If no queue is bound, the exchange drops the message.

## Run tutorial 3

Terminal 1 and terminal 2 (consumers):

```bash
python tutorial-3-publish-subscribe/receive_logs.py
```

Terminal 3 (producer):

```bash
python tutorial-3-publish-subscribe/emit_log.py "info: first log"
```

Both consumers print the same message. To see the bindings:

```bash
rabbitmqctl list_bindings
```
