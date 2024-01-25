from django.db import models


class CurrencyRequest(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    usd_to_rub_rate = models.FloatField()

    def __str__(self):
        return f"{self.timestamp}: {self.usd_to_rub_rate}"

