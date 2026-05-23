# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.core.files.storage import FileSystemStorage
from formtools.wizard.views import SessionWizardView
from django.contrib.auth import login, logout

from .forms import (
    UserRegistrationForm,
    PersonalInfoForm,
    AcademicHistoryForm,
    WorkExperienceForm,
    SkillsForm,
    LanguagesForm,
    UserProfileForm
)

from core.models import (
    UserProfile,
    AcademicHistory,
    WorkExperiences,
    UserSkill,
    UserLanguage
)


class CustomLoginView(LoginView):
    """Vista personalizada de inicio de sesión"""
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("core:home")

    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos")
        return super().form_invalid(form)


def register(request):
    """Vista de registro"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "¡Registro completado con éxito!"
            )

            return redirect('core:home')

        else:
            messages.error(
                request,
                "Por favor corrija los errores."
            )

    else:
        form = UserRegistrationForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )


class HomeView(TemplateView):
    template_name = 'core/home.html'


class CVWizardView(LoginRequiredMixin, SessionWizardView):

    template_name = "core/cv_wizard/wizard_form.html"
    file_storage = FileSystemStorage(
    location='media/profile_photos'
)

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

        initial = super().get_form_initial(step)
        user = self.request.user

        if step == "0":
            initial['first_name'] = user.first_name
            initial['last_name'] = user.last_name
            initial['email'] = user.email

        return initial

    def get_context_data(self, form, **kwargs):

        context = super().get_context_data(
            form=form,
            **kwargs
        )

        current_step = int(self.steps.current)
        total_steps = len(self.form_list)

        context.update({
            "step_title": self.step_titles.get(
                self.steps.current,
                "Formulario"
            ),
            "current_step": current_step + 1,
            "total_steps": total_steps,
            "progress_percentage":
                int((current_step / total_steps) * 100),
            "step_titles": self.step_titles,
        })

        return context

    def done(self, form_list, **kwargs):
        # RESTAURADO: Volvemos a tu lógica original que guardaba perfectamente sin errores
        user = self.request.user

        # =========================
        # PASO 0
        # =========================

        personal_data = form_list[0].cleaned_data

        user.first_name = personal_data['first_name']
        user.last_name = personal_data['last_name']
        user.email = personal_data['email']

        user.save()

        profile, created = UserProfile.objects.get_or_create(
            user_id=user.id
        )

        profile.phone = personal_data.get('phone', '')
        profile.professional_summary = personal_data.get(
            'professional_summary',
            ''
        )

        profile.linkedin_url = personal_data.get(
            'linkedin_url',
            ''
        )

        profile.github_url = personal_data.get(
            'github_url',
            ''
        )
        profile.photo = personal_data.get('photo')

        profile.save()

        # =========================
        # PASO 1
        # =========================
        AcademicHistory.objects.filter(
       user_id=user.id
       ).delete()
        academic_data = form_list[1].cleaned_data

        if academic_data.get('institution_name'):

            AcademicHistory.objects.create(
                user_id=user,
                institution_name=academic_data[
                    'institution_name'
                ],
                speciality=academic_data.get(
                    'speciality',
                    ''
                ),
                degree_id=academic_data['degree_id'],
                academic_field_id=academic_data[
                    'academic_field_id'
                ],
                start_date=academic_data.get('start_date'),
                end_date=academic_data.get('end_date')
            )

        # =========================
        # PASO 2
        # =========================
        WorkExperiences.objects.filter(
        user_id=user.id
    ).delete()
        work_data = form_list[2].cleaned_data

        if work_data.get('enterprise_name'):

            WorkExperiences.objects.create(
                user_id=user,
                enterprise_name=work_data[
                    'enterprise_name'
                ],
                job_title_id=work_data['job_title_id'],
                description=work_data.get(
                    'description',
                    ''
                ),
                achievement=work_data.get(
                    'achievement',
                    ''
                ),
                start_date=work_data.get('start_date'),
                end_date=work_data.get('end_date')
            )

        # =========================
        # PASO 3
        # =========================
        UserSkill.objects.filter(
    user_id=user.id
          ).delete()
        skills_data = form_list[3].cleaned_data

        for skill in skills_data.get('skills', []):

            UserSkill.objects.get_or_create(
                user_id=user,
                skill_id=skill
            )

        # =========================
        # PASO 4
        # =========================
        UserLanguage.objects.filter(
                user_id=user.id
             ).delete()
        languages_data = form_list[4].cleaned_data

        for language in languages_data.get('languages', []):

            UserLanguage.objects.get_or_create(
                user_id=user,
                language_id=language
            )

        messages.success(
            self.request,
            "¡CV creado exitosamente!"
        )

        return redirect("core:cv_list")


class CVDetailView(LoginRequiredMixin, DetailView):

    model = User

    template_name = "core/cv_wizard/cv_detail.html"

    context_object_name = "cv_user"

    pk_url_kwarg = "user_id"

    def get_object(self, queryset=None):

        return get_object_or_404(
            User,
            id=self.kwargs.get('user_id')
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        user = self.get_object()

        context.update({

            "profile":
                UserProfile.objects.filter(
                    user_id=user
                ).first(),

            "academic_histories":
                AcademicHistory.objects.filter(
                    user_id=user
                ).select_related(
                    "degree_id",
                    "academic_field_id"
                ),

            "work_experiences":
                WorkExperiences.objects.filter(
                    user_id=user
                ).select_related(
                    "job_title_id"
                ),

            "skills":
                UserSkill.objects.filter(
                    user_id=user
                ).select_related(
                    "skill_id"
                ),

            "languages":
                UserLanguage.objects.filter(
                    user_id=user
                ).select_related(
                    "language_id"
                ),
        })

        return context


class CVListView(LoginRequiredMixin, ListView):
    """Vista encargada de listar un único CV por persona ordenado por nombre"""
    model = UserProfile
    template_name = "core/cv_list.html"
    context_object_name = "profiles"
    paginate_by = 8

    def get_queryset(self):
        # Mantenemos el orden por nombre de pila (A-Z)
        return UserProfile.objects.all().select_related('user').order_by('user__first_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Inyectamos el último trabajo registrado a cada usuario único
        for profile in context['profiles']:
            ultima_exp = WorkExperiences.objects.filter(
                user_id=profile.user
            ).select_related('job_title_id').order_by('-work_experience_id').first()
            
            profile.ultima_experiencia = ultima_exp
            
        context['total_cvs'] = self.get_queryset().count()
        return context

class ProfileView(LoginRequiredMixin, UpdateView):
  
    model = UserProfile

    form_class = UserProfileForm

    template_name = "core/profile.html"

    def get_object(self, queryset=None):

        profile, created = UserProfile.objects.get_or_create(
            user_id=self.request.user.id
        )

        return profile

    def get_success_url(self):

        return reverse_lazy("core:profile")

    def form_valid(self, form):

        messages.success(
            self.request,
            "Perfil actualizado correctamente"
        )

        return super().form_valid(form)
    
    
@login_required
def delete_cv(request):

    user = request.user

    AcademicHistory.objects.filter(
        user_id=user
    ).delete()

    WorkExperiences.objects.filter(
        user_id=user
    ).delete()

    UserSkill.objects.filter(
        user_id=user
    ).delete()

    UserLanguage.objects.filter(
        user_id=user
    ).delete()

    UserProfile.objects.filter(
        user=user
    ).delete()

    messages.success(
        request,
        "CV eliminado correctamente"
    )

    return redirect('core:home')

@login_required
def custom_logout(request):

    logout(request)

    messages.success(
        request,
        "Sesión cerrada correctamente"
    )

    return redirect('core:home')