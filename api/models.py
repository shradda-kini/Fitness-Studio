from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class FitnessClass(models.Model):
    name = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    instructor = models.CharField(max_length=255)
    available_slots = models.IntegerField()

    def __str__(self):
        return f"{self.name} on {self.datetime.strftime('%Y-%m-%d %H:%M')}"

    def slots_remaining(self):
        return self.available_slots - self.booking_set.count()

    def is_full(self):
        return self.slots_remaining() <= 0


class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()
    booked_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.fitness_class.is_full():
            raise ValidationError("This class is fully booked.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class.name}"


