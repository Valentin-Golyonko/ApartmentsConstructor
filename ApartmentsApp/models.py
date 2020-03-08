from django.db import models


class Apartments(models.Model):
    class Meta:
        verbose_name = 'Apartments'
        verbose_name_plural = 'Apartments'
        ordering = ('id',)

    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)

    choice_list = (
        ('address', 'address'),
        ('room', 'room'),
    )
    parameters = models.CharField(choices=choice_list, max_length=10, default='None')

    def __str__(self):
        return f"{self.name} (Apartments_id {self.id})"


class Room(models.Model):
    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        ordering = ('id',)

    apartment = models.ForeignKey(to='Apartments', on_delete=models.CASCADE,
                                  blank=True, null=True)

    count = models.PositiveSmallIntegerField(default=0)
    squire_size = models.FloatField(default=0.0)

    def __str__(self):
        return f"Room_id {self.id}"


class Chair(models.Model):
    class Meta:
        verbose_name = 'Chair'
        verbose_name_plural = 'Chairs'
        ordering = ('id',)

    room = models.ForeignKey(to='Room', on_delete=models.CASCADE,
                             blank=True, null=True)

    amount = models.PositiveSmallIntegerField(default=0)
