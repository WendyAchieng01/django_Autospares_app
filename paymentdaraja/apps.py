from django.apps import AppConfig


class PaymentdarajaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'paymentdaraja'

    def ready(self):
        import paymentdaraja.signals
