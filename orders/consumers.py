# orders/consumers.py
import requests
from confluent_kafka import Consumer, KafkaError
from django.conf import settings
from .models import Order

# Kafka consumer configuration
consumer = Consumer({
    'bootstrap.servers': settings.KAFKA_BROKER_URL,
    'group.id': 'order_group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe([settings.KAFKA_TOPIC])

def consume_messages():
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        message = msg.value().decode('utf-8')
        user_id, user_email = message.split(',')

        # Get user data from User Service
        try:
            response = requests.get(f'http://localhost:8000/api/users/{user_id}/')
            response.raise_for_status()
            user_data = response.json()
            user = user_data['id']  # Use user ID for creating Order

            Order.objects.create(user_id=user, product='Default Product', quantity=1)
            print(f"Created order for user: {user_email}")
        except requests.RequestException as e:
            print(f"Failed to get user data: {e}")
        except Exception as e:
            print(f"Failed to create order: {e}")

    consumer.close()
