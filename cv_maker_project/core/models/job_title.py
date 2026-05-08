from django.db import models

class JobTitle(models.Model):
     name = models.CharField(max_length=150, unique=True)
     description = models.TextField(blank=True, null=True)
     is_active = models.BooleanField(default=True)

class Meta:
    db_table = 'job_title'
    verbose_name = 'Job Title'
    verbose_name_plural = 'Job Titles'

def __str__(self) :
    return self.name
