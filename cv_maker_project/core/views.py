
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_484
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView

from formtools.wizard.views import SessionWizardView

from .forms import (
    UserRegistrationForm, PersonalInfoForm, AcademicHistoryForm,
    WorkExperienceForm, SkillsForm, LanguagesForm, UserProfileForm
)
from core.models import (
    UserProfile, AcademicHistory, WorkExperiences, UserSkill,
    Skill, UserLanguage, Languages
)
class CustomLoginView(LoginView):
    """Vista personalizada de inicio de sesión"""
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        """Redirige a la página principal después de iniciar sesión"""
        return reverse_lazy("core:home")

    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos")
        return super().form_invalid(form)
    
    def register(request):
     """Vista de registro de usuario"""
     if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Registro completado con éxito!")
            return redirect('core:home')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
     else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

class HomeView(TemplateView):
    """Vista de página principal"""
    template_name = 'core/home.html'

    class CVCreateWizardView(LoginRequiredMixin, SessionWizardView):
      """
      Wizard para creación de CV en múltiples pasos:
      0: Información Personal
      1: Historial Académico
      2: Experiencia Laboral
      3: Habilidades
      4: Idiomas
      """
    template_name = "core/cv_wizard/wizard_form.html"
    
    form_list = [
        PersonalInfoForm,
        AcademicHistoryForm,
        WorkExperienceForm,
        SkillsForm,
        LanguagesForm,
    ]
    
    step_titles = {
        "0": "Información Personal",
        "1": "Historial Académico",
        "2": "Experiencia Laboral",
        "3": "Habilidades Técnicas",
        "4": "Idiomas",
    }

    def get_template_names(self):
        return [self.template_name]

    def get_form_initial(self, step):
        """Pre-carga datos iniciales del usuario autenticado"""
        initial = super().get_form_initial(step)
        user = self.request.user
        
        if step == "0":
            initial['first_name'] = user.first_name
            initial['last_name'] = user.last_name
            initial['email'] = user.email
            if hasattr(user, 'profile'):
                initial['phone'] = user.profile.phone
                initial['professional_summary'] = user.profile.professional_summary
                initial['linkedin_url'] = user.profile.linkedin_url
                initial['github_url'] = user.profile.github_url
        return initial
    
    def get_context_data(self, form, **kwargs):
        """Agrega contexto adicional sobre el progreso del wizard"""
        context = super().get_context_data(form=form, **kwargs)
        current_step = int(self.steps.current)
        total_steps = len(self.form_list)
        
        context.update({
            "step_title": self.step_titles.get(self.steps.current, "Formulario"),
            "current_step": current_step + 1,
            "total_steps": total_steps,
            "progress_percentage": int((current_step / total_steps) * 100),
            "step_titles": self.step_titles,
        })
        return context
    
    def done(self, form_list, **kwargs):
        """Procesa todos los datos al finalizar el wizard"""
        user = self.request.user
        
        # Paso 0: Información Personal
        personal_data = form_list[0].cleaned_data
        
        # Actualizar User
        user.first_name = personal_data['first_name']
        user.last_name = personal_data['last_name']
        user.email = personal_data['email']
        user.save()
        
        # Actualizar o crear Perfil
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.phone = personal_data.get('phone', '')
        profile.professional_summary = personal_data.get('professional_summary', '')
        profile.linkedin_url = personal_data.get('linkedin_url', '')
        profile.github_url = personal_data.get('github_url', '')
        profile.save()
        
        # Paso 1: Historial Académico
        academic_data = form_list[1].cleaned_data
        if academic_data.get('institution_name'):
            AcademicHistory.objects.create(
                user=user,
                institution_name=academic_data['institution_name'],
                specialty=academic_data.get('specialty', ''),
                degree_id=academic_data['degree_id'],
                academic_field_id=academic_data['academic_field_id'],
                start_date=academic_data.get('start_date'),
                end_date=academic_data.get('end_date')
            )
            
        # Paso 2: Experiencia Laboral
        work_data = form_list[2].cleaned_data
        if work_data.get('enterprise_name'):
            WorkExperiences.objects.create(
                user=user,
                enterprise_name=work_data['enterprise_name'],
                job_title_id=work_data['job_title_id'],
                description=work_data.get('description', ''),
                achievement=work_data.get('achievement', ''),
                start_date=work_data.get('start_date'),
                end_date=work_data.get('end_date')
            )

            # Paso 3: Habilidades
        skills_data = form_list[3].cleaned_data
        for skill in skills_data.get('skills', []):
            UserSkill.objects.get_or_create(
                user=user,
                skill_id=skill
            )
            
        # Paso 4: Idiomas
        languages_data = form_list[4].cleaned_data
        for language in languages_data.get('languages', []):
            UserLanguage.objects.get_or_create(
                user=user,
                language_id=language
            )
            
        messages.success(self.request, "¡CV creado exitosamente!")
        return redirect("core:cv_detail", user_id=user.id)
    
    class CVDetailView(LoginRequiredMixin, DetailView):
      """Vista de detalle del CV de un usuario"""
      model = User
      template_name = "core/cv_wizard/cv_detail.html"
      context_object_name = "cv_user"
      pk_url_kwarg = "user_id"
    
    def get_object(self, queryset=None):
        return get_object_or_484(User, id=self.kwargs.get('user_id'))
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        
        context.update({
            "profile": getattr(user, 'profile', None),
            "academic_histories": AcademicHistory.objects.filter(user=user).select_related("degree_id", "academic_field_id"),
            "work_experiences": WorkExperiences.objects.filter(user=user).select_related("job_title_id"),
            "skills": UserSkill.objects.filter(user=user).select_related("skill_id"),
            "languages": UserLanguage.objects.filter(user=user).select_related("language_id"),
        })
        return context
    
    class CVListView(LoginRequiredMixin, ListView):
     """Vista de listado de CVs existentes"""
    model = User
    template_name = "core/cv_list.html"
    context_object_name = "users"
    paginate_by = 10
    
    def get_queryset(self):
        return User.objects.filter(is_active=True).order_by('date_joined')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_cvs'] = self.get_queryset().count()
        return context
    
    class ProfileView(LoginRequiredMixin, UpdateView):
     """Vista para editar el perfil del usuario"""
    model = UserProfile
    form_class = UserProfileForm
    template_name = "core/profile.html"
    
    def get_object(self, queryset=None):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
        
    def get_success_url(self):
        return reverse_lazy("core:profile")
        
    def form_valid(self, form):
        messages.success(self.request, "Perfil actualizado correctamente")
        return super().form_valid(form)
    
