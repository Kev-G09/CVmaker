from django.db import models
from django.conf import settings
import uuid

class UserLanguage(models.Model):
    """
    Tabla intermedia para la relación muchos a muchos entre Usuarios e Idiomas.
    Incluye nivel de dominio del idioma.
    """
    LEVEL_CHOICES = [
        ('BASIC', 'Básico'),
        ('INTERMEDIATE', 'Intermedio'),
        ('ADVANCED', 'Avanzado'),
        ('FLUENT', 'Fluido'),
        ('NATIVE', 'Nativo'),
    ]
    
    user_language_id = models.AutoField(primary_key=True)
    external_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='INTERMEDIATE')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    # Relaciones
    language_id = models.ForeignKey(
        'Languages',
        on_delete=models.CASCADE,
        db_column='language_id',
        related_name='user_languages'
    )
    
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name='user_languages'
    )
    
    class Meta:
        db_table = 'users_info_languages'
        verbose_name = 'Idioma del Usuario'
        verbose_name_plural = 'Idiomas de Usuarios'
        unique_together = [['user_id', 'language_id']]
        
    def __str__(self):
        return f"{self.user_id} - {self.language_id} ({self.get_level_display()})"