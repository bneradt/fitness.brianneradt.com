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
        blank=False,
        choices=PullupType.choices,
        default=PullupType.PULLUPS,
    )

    pullup_count1 = models.PositiveIntegerField(default=0)
    pushup_count1 = models.PositiveIntegerField(default=0)

    pullup_count2 = models.PositiveIntegerField(default=0)
    pushup_count2 = models.PositiveIntegerField(default=0)

    pullup_count3 = models.PositiveIntegerField(default=0)
    pushup_count3 = models.PositiveIntegerField(default=0)

    # add fields to store daily totals
    total_pullups = models.PositiveIntegerField(default=0, editable=False)
    total_pushups = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def save(self, *args, **kwargs):
        # calculate and store totals before saving
        self.total_pullups = (
            self.pullup_count1 + self.pullup_count2 + self.pullup_count3
        )
        self.total_pushups = (
            self.pushup_count1 + self.pushup_count2 + self.pushup_count3
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.total_pullups} Pullups, {self.total_pushups} Pushups"
