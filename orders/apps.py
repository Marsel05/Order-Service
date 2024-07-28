from django.apps import AppConfig

class OrdersConfig(AppConfig):
    name = 'orders'

    def ready(self):
        from .signals import kafka_consumer
        kafka_consumer.start()
