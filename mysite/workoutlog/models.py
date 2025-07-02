from django.db import models  # type: ignore
from django.conf import settings  # type: ignore

# Create your models here.

class PullupType(models.TextChoices):
    PULLUPS = 'PU', 'Pullups'
    CHINUPS = 'CH', 'Chinups'
    NEUTRAL = 'NE', 'Neutral'

class WorkoutSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    pullup_type = models.CharField(
        max_length=2,
        choices=PullupType.choices,
        default=PullupType.PULLUPS,
    )
    pullup_count = models.PositiveIntegerField(default=0)
    pushup_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date} (Pullups: {self.pullup_count} {self.get_pullup_type_display()}, Pushups: {self.pushup_count})"
