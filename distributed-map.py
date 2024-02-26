import hazelcast

if __name__ == "__main__":
    client = hazelcast.HazelcastClient()
    distributed_map = client.get_map("my-distributed-map").blocking()
    for i in range(1000):
        distributed_map.put(i, i)
    client.shutdown()
