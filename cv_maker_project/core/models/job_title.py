from django.db import models
import uuid

class JobTitle(models.Model):
    """
    Catálogo de puestos o títulos de trabajo.
    Ejemplos: Desarrollador Full Stack, Arquitecto de Software, Gerente de Proyecto
    """
    # Identificadores
    external_id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False)
    
    # Datos principales
    name = models.CharField(max_length=150, unique=True, verbose_name="Nombre del puesto")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    # Auditoría
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name="Fecha de actualización")

    class Meta:
        db_table = 'job_title'
        verbose_name = 'Puesto de Trabajo'
        verbose_name_plural = 'Puestos de Trabajo'
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name, description=None, is_active=True):
        """Método de fábrica para crear un nuevo puesto de trabajo"""
        return cls(name=name, description=description, is_active=is_active)