from django.db import models  # type: ignore
from django.conf import settings  # type: ignore

# Create your models here.

class PullupType(models.TextChoices):
    PULLUPS = 'PU', 'Pullups'
    CHINUPS = 'CH', 'Chinups'
    NEUTRAL = 'NE', 'Neutral'

class WorkoutSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(unique=True)
    pullup_type = models.CharField(
        max_length=2,
        choices=PullupType.choices,
        default=PullupType.PULLUPS,
    )

    pullup_count1 = models.PositiveIntegerField(default=0)
    pushup_count1 = models.PositiveIntegerField(default=0)

    pullup_count2 = models.PositiveIntegerField(default=0)
    pushup_count2 = models.PositiveIntegerField(default=0)

    pullup_count3 = models.PositiveIntegerField(default=0)
    pushup_count3 = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        total_pullups = (self.pullup_count1 +
                         self.pullup_count2 +
                         self.pullup_count3)
        total_pushups = (self.pushup_count1 +
                         self.pushup_count2 +
                         self.pushup_count3)
        return f"{self.user.username} - {self.date}: {total_pullups} Pullups, {total_pushups} Pushups"
