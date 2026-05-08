from django.db import models
import uuid

class Languages(models.Model):
    """Catálogo de idiomas."""
    languages_id = models.AutoField(primary_key=True)
    external_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    description = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Idioma"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        db_table = 'languages'
        verbose_name = 'Idioma'
        verbose_name_plural = 'Idiomas'
        ordering = ['description']
        
    def __str__(self):
        return self.description