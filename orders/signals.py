import atexit
import threading
from confluent_kafka import Consumer, KafkaError
from django.conf import settings
from .models import Order

class KafkaConsumer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.consumer = Consumer({
            'bootstrap.servers': settings.KAFKA_BROKER_URL,
            'group.id': 'order_group',
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe([settings.KAFKA_TOPIC])
        self.running = True

    def run(self):
        while self.running:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            user_email = msg.value().decode('utf-8')
            Order.objects.create(user_email=user_email, product='Default Product', quantity=1)
            print(f"Created order for user: {user_email}")

        self.consumer.close()

    def stop(self):
        self.running = False

kafka_consumer = KafkaConsumer()

# Registering the consumer stop function to be called on exit
atexit.register(kafka_consumer.stop)




