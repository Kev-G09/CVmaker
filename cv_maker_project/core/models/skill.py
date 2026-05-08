from django.db import models
import uuid

class Skill(models.Model):
    """Catálogo de habilidades."""
    skill_id = models.AutoField(primary_key=True)
    external_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    description = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Habilidad"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        db_table = 'skill'
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades'
        ordering = ['description']
        
    def __str__(self):
        return self.description
        
    @classmethod
    def create(cls, description):
        return cls(description=description)