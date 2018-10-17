from __future__ import unicode_literals
from django.db import models


class Symptom(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=120,null=False)
	updated=models.DateTimeField(auto_now=True,auto_now_add=False)
	timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)
    	
	def __unicode__(self):
		return self.name
	def __str__(self):
		return self.name