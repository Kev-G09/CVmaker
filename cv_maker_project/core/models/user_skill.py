from django.db import models
from django.conf import settings
import uuid

class UserSkill(models.Model):
    
    PROFICIENCY_CHOICES = [
        (1, 'Básico'),
        (2, 'Intermedio'),
        (3, 'Avanzado'),
        (4, 'Experto'),
    ]

    user_skill_id = models.AutoField(primary_key=True)
    external_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    proficiency_level = models.IntegerField(
        default=3,
        choices=PROFICIENCY_CHOICES,
        verbose_name="Nivel de Competencia",
        help_text="Autoevaluación de su dominio en esta habilidad (1: Básico - 4: Experto)"
    )
    
    skill_id = models.ForeignKey(
        'Skill',
        on_delete=models.CASCADE,
        db_column='skill_id',
        verbose_name="Habilidad"
    )
    
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        verbose_name="Usuario"
    )
    
    class Meta:
        db_table = 'users_skills'
        verbose_name = 'Habilidad de Usuario'
        verbose_name_plural = 'Habilidades de Usuarios'