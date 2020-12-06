from datetime import datetime
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class Game(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=200, blank=True, default='', unique=True)
	release_date = models.DateTimeField()
	game_category = models.CharField(max_length=200, blank=True, default='')
	played = models.BooleanField(default=False)

	class Meta:
		ordering = ('name',)

	def delete(self):
		time_now = timezone.make_aware(
                    datetime.now(),
                    timezone.get_current_timezone()
                )
		if time_now > self.release_date:
			raise ValidationError("Cannot delete released games.")
		return super().delete()