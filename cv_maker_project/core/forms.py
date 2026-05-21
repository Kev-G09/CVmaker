from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from core.models import (
    UserProfile, AcademicHistory, AcademicField, Degrees,
    WorkExperiences, JobTitle, UserSkill, Skill, UserLanguage, Languages
)

class UserRegistrationForm(UserCreationForm):
    """Formulario de registro de usuario"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    """Formulario de perfil de usuario"""
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'birth_date', 'professional_summary', 'linkedin_url', 'github_url', 'personal_website']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+505 8888-7777'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'professional_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/usuario'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/usuario'}),
            'personal_website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.usuario.com'}),
        }

class PersonalInfoForm(forms.Form):
    """Formulario de información personal (Paso 1 del wizard)"""
    first_name = forms.CharField(max_length=30, required=True, label="Nombre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, label="Apellido", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label="Correo Electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=20, required=False, label="Teléfono", widget=forms.TextInput(attrs={'class': 'form-control'}))
    professional_summary = forms.CharField(required=False, label="Resumen Profesional", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    linkedin_url = forms.URLField(required=False, label="LinkedIn", widget=forms.URLInput(attrs={'class': 'form-control'}))
    github_url = forms.URLField(required=False, label="GitHub", widget=forms.URLInput(attrs={'class': 'form-control'}))

    class AcademicHistoryForm(forms.ModelForm):
      """Formulario de historial académico (Paso 2 del wizard)"""
    class Meta:
        model = AcademicHistory
        fields = ['institution_name', 'specialty', 'degree_id', 'academic_field_id', 'start_date', 'end_date']
        widgets = {
            'institution_name': forms.TextInput(attrs={'class': 'form-control'}),
            'specialty': forms.TextInput(attrs={'class': 'form-control'}),
            'degree_id': forms.Select(attrs={'class': 'form-select'}),
            'academic_field_id': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['degree_id'].queryset = Degrees.objects.all()
        self.fields['degree_id'].label = "Grado Académico"
        self.fields['academic_field_id'].queryset = AcademicField.objects.all()
        self.fields['academic_field_id'].label = "Campo Académico"
        self.fields['end_date'].required = False

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date < start_date:
            self.add_error('end_date', 'La fecha de finalización no puede ser anterior a la fecha de inicio')
        return cleaned_data
    
    class WorkExperienceForm(forms.ModelForm):
     """Formulario de experiencia laboral (Paso 3 del wizard)"""
    class Meta:
        model = WorkExperiences
        fields = ['enterprise_name', 'job_title_id', 'description', 'achievement', 'start_date', 'end_date']
        widgets = {
            'enterprise_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title_id': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'achievement': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['job_title_id'].queryset = JobTitle.objects.filter(is_active=True)
        self.fields['job_title_id'].label = "Puesto/Título"
        self.fields['end_date'].required = False

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date < start_date:
            self.add_error('end_date', 'La fecha de finalización no puede ser anterior a la fecha de inicio')
        return cleaned_data
    
    class SkillsForm(forms.Form):
     """Formulario de habilidades (Paso 4 del wizard)"""
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Habilidades Técnicas"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

class LanguagesForm(forms.Form):
    """Formulario de idiomas (Paso 5 del wizard)"""
    languages = forms.ModelMultipleChoiceField(
        queryset=Languages.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Idiomas"
    )