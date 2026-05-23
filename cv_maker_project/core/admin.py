from django.contrib import admin
# Importamos cada modelo desde su archivo específico
from .models.user_profile import UserProfile
from .models.user_skill import UserSkill
from .models.work_experiences import WorkExperiences
from .models.academic_history import AcademicHistory
from .models.skill import Skill
from .models.languages import Languages
from .models.user_language import UserLanguage

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'skill_id', 'proficiency_level')
    list_filter = ('proficiency_level', 'skill_id')

@admin.register(WorkExperiences)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'enterprise_name', 'job_title_id', 'start_date')

admin.site.register(AcademicHistory)
admin.site.register(Skill)
admin.site.register(Languages)
admin.site.register(UserLanguage)