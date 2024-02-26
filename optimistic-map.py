import threading
import hazelcast


def increment_key_optimistic():
    client = hazelcast.HazelcastClient()
    optimistic_distributed_map = client.get_map("my-optimistic-distributed-map").blocking()
    optimistic_distributed_map.put_if_absent("key", 0)
    for _ in range(10000):
        while True:
            initial_value = optimistic_distributed_map.get("key")
            new_value = initial_value
            new_value += 1
            if optimistic_distributed_map.replace_if_same("key", initial_value, new_value):
                break
    client.shutdown()


if __name__ == "__main__":
    threads = []
    for i in range(3):
        thread = threading.Thread(target=increment_key_optimistic)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    client = hazelcast.HazelcastClient()
    res = client.get_map("my-optimistic-distributed-map").blocking().get("key")
    client.shutdown()

    print(f"The final value of the key is {res}")
