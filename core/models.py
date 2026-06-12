from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Booking(models.Model):

    TIME_CHOICES = [
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Evening', 'Evening'),
    ]

    OFFICE_CHOICES = [
        ('0979661111', '0979661111'),
        ('0978661111', '0978661111'),
    ]

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    office_phone = models.CharField(
        max_length=10,
        choices=OFFICE_CHOICES,
        default='0979661111'
    )

    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)

    time = models.CharField(
        max_length=20,
        choices=TIME_CHOICES,
        default='Morning'
    )

    total_price = models.FloatField()

    # keep advance (NOT used in calculation)
    advance = models.FloatField(default=0)

    extra = models.FloatField(default=0)

    # final calculated balance
    balance = models.FloatField(default=0)

    date = models.DateField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    # ✅ AUTO CALCULATE BALANCE (IMPORTANT FIX)
    def save(self, *args, **kwargs):
        self.balance = self.total_price + self.extra
        super().save(*args, **kwargs)

    def __str__(self):
        return self.customer_name


class Expense(models.Model):

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE
    )

    labor = models.FloatField(default=0)

    packers = models.FloatField(default=0)

    supervisor = models.FloatField(default=0)

    driver = models.FloatField(default=0)

    stairs = models.FloatField(default=0)


    additional = models.FloatField(default=0)
    
    time = models.CharField(max_length=50, default='')

    derdare = models.IntegerField(default=0)

    night = models.IntegerField(default=0)

    long_way = models.IntegerField(default=0)

    carpenter = models.IntegerField(default=0)

    total = models.FloatField(default=0)

    date = models.DateField()

    def __str__(self):

        return f"Expense for Move {self.booking.id}"
    


class MonthlyExpense(models.Model):

    month = models.IntegerField()

    fuel = models.IntegerField(default=0)

    repair = models.IntegerField(default=0)

    oil = models.IntegerField(default=0)

    office_rent = models.IntegerField(default=0)

    house_rent = models.IntegerField(default=0)

    other = models.IntegerField(default=0)

    total = models.IntegerField(default=0)

    def __str__(self):

        return str(self.month)
    

class Profile(models.Model):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='employee'
    )

    def __str__(self):
        return self.user.username
    


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:

        Profile.objects.create(user=instance)

class BusinessRule(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    def __str__(self):

        return self.title
    



time = models.CharField(max_length=50, default='')

extra = models.IntegerField(default=0)

balance = models.IntegerField(default=0)