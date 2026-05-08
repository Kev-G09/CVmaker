from django.db import models
from django.conf import settings
import uuid

class AcademicHistory(models.Model):
   
    academic_history_id = models.AutoField(primary_key=True)
    external_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    institution_name = models.CharField(
        max_length=255, 
        verbose_name="Nombre de la Institución",
        help_text="Universidad, instituto o centro de estudios"
    )
    
    speciality = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        verbose_name="Especialidad/Mención"
    )
    
    start_date = models.DateField(null=True, blank=True, verbose_name="Fecha de inicio")
    end_date = models.DateField(null=True, blank=True, verbose_name="Fecha de finalización")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    
    degree_id = models.ForeignKey(
        'Degrees', 
        on_delete=models.PROTECT, 
        db_column='degree_id', 
        verbose_name="Grado"
    )
    
    academic_field_id = models.ForeignKey(
        'AcademicField', 
        on_delete=models.PROTECT, 
        db_column='academic_field_id',
        verbose_name="Campo Académico"
    )
    
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        db_column='user_id',
        verbose_name="Usuario", 
        related_name='academic_histories'
    )

    class Meta:
        db_table = 'academic_history'
        verbose_name = 'Historial Académico'
        verbose_name_plural = 'Historiales Académicos'
        ordering = ['-start_date', 'user_id']
        unique_together = []

    def __str__(self):
        return f"{self.user_id} - {self.degree_id} en {self.academic_field_id}"