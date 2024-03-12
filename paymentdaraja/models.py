from django.db import models

from orders.models import Order

# Create your models here.
class AccessToken(models.Model):
	token = models.CharField(max_length=30)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		get_latest_by = 'created_at'

	def __str__(self):
		return self.token
	
class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
    phone_number = models.CharField(max_length=12)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_receipt_number = models.CharField(max_length=50)
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
	
    def __str__(self):
        return f"Transaction {self.mpesa_receipt_number} - {self.amount}"