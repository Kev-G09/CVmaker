from django.db import models
from django.conf import settings
import uuid

class UserProfile(models.Model):
    """
    Extensión del modelo User de Django para añadir campos personalizados.
    Relación OneToOne con el modelo User existente.
    """
    # Esta es la clave primaria y también la clave foránea a User
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile'
    )
    
    external_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    # Campos adicionales que no están en el User original
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    address = models.TextField(blank=True, null=True, verbose_name="Dirección")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Fecha de nacimiento")
    professional_summary = models.TextField(blank=True, null=True, verbose_name="Resumen profesional")
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, verbose_name="Foto de perfil")
    
    # Redes sociales
    linkedin_url = models.URLField(blank=True, null=True, verbose_name="LinkedIn")
    github_url = models.URLField(blank=True, null=True, verbose_name="GitHub")
    personal_website = models.URLField(blank=True, null=True, verbose_name="Sitio web personal")
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'

    def __str__(self):
        return f"Perfil de {self.user.get_full_name() or self.user.username}"