from django.db import models
from django.urls import reverse
from datetime import date, time
from django.contrib.auth.models import User

# Create your models here.
class GameGroup(models.Model):
    name = models.CharField(max_length=30, unique=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.IntegerField()
    users = models.ManyToManyField(User)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    description = models.TextField(max_length=3000) 

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('groups_detail', kwargs={'group_id': self.id})

class Event(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateField('date')
    time = models.TimeField('time', auto_now_add=False, editable=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.IntegerField()
    game = models.TextField(max_length=200)
    game_description = models.TextField(max_length=3000)
    limit = models.IntegerField()
    group = models.ForeignKey(GameGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
  # change the default sort
    class Meta:
        ordering = ['-date']

class Genre(models.Model):
    genres = models.CharField(max_length=50)
    group = models.ForeignKey(GameGroup, on_delete=models.CASCADE)

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(GameGroup, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'group'], name='unique_application')
        ]

class Photo(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(GameGroup, on_delete=models.CASCADE)

class Attending(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    group = models.ForeignKey(GameGroup, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'event'], name='unique_attendee')
        ]

    # we gotta get this later
    # def check_limit(self, event_id):
    #     return self.event_set.filter(event=event_id).count() < Event.objects.get(id=event_id).limit

    # example from finches lab
    # finches = Finch.objects.filter(user=request.user)
    # return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)
 