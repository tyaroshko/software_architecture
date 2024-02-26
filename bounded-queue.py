import hazelcast
import threading


def produce(queue, event):
    for i in range(1, 101):
        put_success = queue.offer(i)
        current_size = queue.size()
        if put_success:
            print(f"Producer thread added value {i} to the queue; current queue size: {current_size}")
        else:
            print(f"Producer thread failed to add {i} to the queue as the queue is full!")
    event.set()


def consume(queue, r_id, event):
    while not event.is_set() or not queue.is_empty():
        num = queue.poll(1)
        if not num:
            if event.is_set():
                break
            else:
                continue
        print(f"Consumer thread {r_id} consumed {num}")


if __name__ == "__main__":
    client = hazelcast.HazelcastClient()

    queue = client.get_queue("my-queue").blocking()
    queue.clear()

    event = threading.Event()

    producer = threading.Thread(target=produce, args=(queue, event))
    producer.start()

    consumers = []
    for i in range(2):
        thread = threading.Thread(target=consume, args=(queue, i, event))
        consumers.append(thread)
        
    for thread in consumers:
        thread.start()
    for thread in consumers:
        thread.join()

    producer.join()

    queue.clear()

    print("Consumer threads finished working")

    producer = threading.Thread(target=produce, args=(queue, event))
    producer.start()
    producer.join()

    print("Producer finished. No consumers to read the queue. The queue is full...")