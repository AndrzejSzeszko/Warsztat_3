from django.db import models


class Reservation(models.Model):
    room = models.ForeignKey('Room', null=False, on_delete=models.CASCADE)
    date = models.DateField(null=False)
    commentary = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        unique_together = (('room', 'date'),)


class RoomManager(models.Manager):
    def search(self, name=None, capacity=None, projector=None, date=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(name__contains=name) if name else queryset
        queryset = queryset.filter(capacity__gte=capacity) if capacity else queryset
        queryset = queryset.filter(projector=projector) if projector is not None else queryset

        if date:
            free_rooms_ids_queryset = Reservation.objects.exclude(date=date).values('room_id').distinct()
            queryset = queryset.filter(id__in=free_rooms_ids_queryset)

        return queryset.distinct().order_by('pk')


class Room(models.Model):
    name = models.CharField(max_length=128)
    capacity = models.IntegerField(null=True, blank=True)
    projector = models.BooleanField(null=True, blank=True, default=True)
    objects = RoomManager()
