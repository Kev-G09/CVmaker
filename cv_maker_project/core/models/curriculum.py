from django.db import models
from django.conf import settings

class Curriculum(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Mi Nuevo CV")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # Los más nuevos saldrán primero

    def __str__(self):
        return f"{self.title} de {self.user.username}"