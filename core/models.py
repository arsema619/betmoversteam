from django.db import models

class Booking(models.Model):
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    total_price = models.FloatField()
    advance = models.FloatField()
    balance = models.FloatField()
    date = models.DateField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.customer_name


class Expense(models.Model):
    labor = models.FloatField(default=0)
    packers = models.FloatField(default=0)
    driver = models.FloatField(default=0)
    supervisor = models.FloatField(default=0)
    additional = models.FloatField(default=0)
    miscellaneous = models.FloatField(default=0)
    total = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return str(self.date)