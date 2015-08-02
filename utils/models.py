from django.db import models

# Create your models here.


class Dated(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	deleted_at = models.DateTimeField(null=True)

	class Meta:
		abstract = True
