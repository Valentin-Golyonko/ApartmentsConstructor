from django.db import models


class Apartments(models.Model):
    class Meta:
        verbose_name = 'Apartments'
        verbose_name_plural = 'Apartments'
        ordering = ('id',)

    def __str__(self):
        return f"{self.name} (Apartments_id {self.id})"

    name = models.CharField(max_length=50)
    # address = models.ForeignKey(to='Address', on_delete=models.CASCADE, blank=True, null=True)
    # room = models.ForeignKey(to='Room', on_delete=models.CASCADE, blank=True, null=True)

    choice_list = (
        ('address', 'address'),
        ('room', 'room'),
    )
    parameters = models.CharField(choices=choice_list, max_length=10, default='None')


class Address(models.Model):
    apartment = models.ForeignKey(to=Apartments, on_delete=models.CASCADE)

    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)

    def __str__(self):
        return f"Address_id: {self.id}"


class Room(models.Model):
    apartment = models.ForeignKey(to=Apartments, on_delete=models.CASCADE)

    count = models.PositiveSmallIntegerField()
    squire_size = models.FloatField()

    def __str__(self):
        return f"Room_id {self.id}"
