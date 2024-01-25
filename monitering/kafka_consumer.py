from confluent_kafka import Consumer, KafkaError
import os

conf = {
    'bootstrap.servers': 'fall2023-comp585.cs.mcgill.ca:9092',  # Kafka broker
    'group.id': 'log_consumer_group',
    'auto.offset.reset': 'latest'
}

consumer = Consumer(conf)

consumer.subscribe(['movielog2'])

log_dir = "/path/to/kafka/logs/"
os.makedirs(log_dir, exist_ok=True)
base_log_path = os.path.join(log_dir, 'kafka_logs.log')

# MAX_SIZE: 50MB*5
MAX_LOG_SIZE = 50 * 1024 * 1024
MAX_LOG_FILES = 5

def rotate_logs():
    for i in range(MAX_LOG_FILES - 2, -1, -1):
        src = f"{base_log_path}.{i}"
        dst = f"{base_log_path}.{i + 1}"
        if os.path.exists(src):
            os.rename(src, dst)

    if os.path.exists(base_log_path):
        os.rename(base_log_path, base_log_path + ".0")


try:
    with open(base_log_path, 'a') as log_file:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print('Reached end of partition')
                else:
                    print('Error while consuming message:', msg.error())
            else:
                # Check if log size exceeds limit
                if log_file.tell() + len(msg.value()) > MAX_LOG_SIZE:
                    log_file.close()
                    rotate_logs()
                    log_file = open(base_log_path, 'a')

                log_file.write(msg.value().decode('utf-8') + '\n')
                log_file.flush()

except KeyboardInterrupt:
    pass

finally:
    consumer.close()