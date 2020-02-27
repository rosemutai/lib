from django.db import models

class Stk(models.Model):
    MerchantRequestID = models.CharField(max_length=250, null=True)
    CheckoutRequestID = models.CharField(max_length=250, null=True)
    ResultCode = models.IntegerField(null=True)
    ResultDesc = models.CharField(max_length=250, null=True)
    Amount = models.CharField(max_length=250, null=True)
    MpesaReceiptNumber = models.CharField(max_length=250, null=True)
    Balance = models.CharField(max_length=250, null=True)
    TransactionDate = models.CharField(max_length=250, null=True)
    PhoneNumber = models.CharField(max_length=250, null=True)

    class Meta:
        ordering = ['TransactionDate']

    def __str__(self):
        return str(self.CheckoutRequestID)