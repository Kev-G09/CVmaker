from django.db import models
from django.conf import settings
import uuid

class WorkExperiences(models.Model):
    
    work_experience_id = models.AutoField(primary_key=True)
    external_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    enterprise_name = models.CharField(
        max_length=255,
        verbose_name="Empresa",
        help_text="Nombre de la empresa o institución donde laboró"
    )
    
    responsibilities = models.TextField(
        blank=True,
        null=True,
        verbose_name="Responsabilidades",
        help_text="Liste sus principales funciones y responsabilidades en el cargo"
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción del Puesto",
        help_text="Breve resumen de su rol dentro de la organización"
    )
    
    achievement = models.TextField(
        blank=True,
        null=True,
        verbose_name="Logros",
        help_text="Mencione metas alcanzadas o proyectos exitosos"
    )
    
    start_date = models.DateField(
        verbose_name="Fecha de Inicio",
        help_text="Fecha en la que comenzó a laborar"
    )
    
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Finalización",
        help_text="Dejar en blanco si es su empleo actual"
    )
    
    job_title_id = models.ForeignKey(
        'JobTitle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='job_title_id',
        verbose_name="Puesto de Trabajo"
    )
    
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        verbose_name="Usuario"
    )

    class Meta:
        db_table = 'work_experiences'
        verbose_name = 'Experiencia Laboral'
        verbose_name_plural = 'Experiencias Laborales'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.enterprise_name} - {self.user_id}"