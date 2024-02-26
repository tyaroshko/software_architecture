import threading
import hazelcast


def increment_key():
    client = hazelcast.HazelcastClient()
    distributed_map_with_locks = client.get_map("my-distributed-map-with-locks").blocking()
    distributed_map_with_locks.put_if_absent("key", 0)
    for _ in range(10000):
        value = distributed_map_with_locks.get("key")
        value += 1
        distributed_map_with_locks.put("key", value)
    client.shutdown()


if __name__ == "__main__":
    threads = []
    for i in range(3):
        thread = threading.Thread(target=increment_key)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    client = hazelcast.HazelcastClient()
    res = client.get_map("my-distributed-map-with-locks").blocking().get("key")
    client.shutdown()

    print(f"The final value of the key is {res}")
