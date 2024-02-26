import threading
import hazelcast


def increment_key_pessimistic():
    client = hazelcast.HazelcastClient()
    pessimistic_distributed_map = client.get_map("my-pessimistic-distributed-map").blocking()
    pessimistic_distributed_map.put_if_absent("key", 0)
    for _ in range(10000):
        try:
            pessimistic_distributed_map.lock("key")
            value = pessimistic_distributed_map.get("key")
            value += 1
            pessimistic_distributed_map.put("key", value)
        finally:
            pessimistic_distributed_map.unlock("key")
    client.shutdown()


if __name__ == "__main__":
    threads = []
    for i in range(3):
        thread = threading.Thread(target=increment_key_pessimistic)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    client = hazelcast.HazelcastClient()
    res = client.get_map("my-pessimistic-distributed-map").blocking().get("key")
    client.shutdown()

    print(f"The final value of the key is {res}")
