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

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class WorkoutSet(models.Model):
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='sets')
    set_number = models.PositiveSmallIntegerField(
        choices=[(1, 'Set 1'), (2, 'Set 2'), (3, 'Set 3')]
    )
    pullup_count = models.PositiveIntegerField(default=0)
    pushup_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('session', 'set_number')
        ordering = ['session', 'set_number']

    def __str__(self):
        user = self.session.user.username
        date = self.session.date
        return f"{user} - {date} - Set {self.set_number}"
