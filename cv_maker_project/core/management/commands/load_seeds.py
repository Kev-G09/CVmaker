
import json
import uuid
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from core.models import (
    AcademicField,
    Degrees,
    JobTitle,
    Languages,
    Skill
)

class Command(BaseCommand):
    help = 'Carga datos semilla para catálogos'

    FIXTURES = {
        '01_academic_fields': AcademicField,
        '02_degrees': Degrees,
        'job_titles': JobTitle,
        'languages': Languages,
        'skills': Skill,
    }

    TABLES = [
        'academic_field',
        'degrees',
        'job_title',
        'languages',
        'skill'
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Elimina datos antes de cargar'
        )

    def handle(self, *args, **options):
        has_errors = False
        if options['force']:
            self.clear_all_catalogs()

        self.stdout.write(self.style.SUCCESS('=== CARGANDO SEEDS ==='))
        
        for fixture_name, model_class in self.FIXTURES.items():
            try:
                self.load_fixture(fixture_name, model_class)
                self.stdout.write(self.style.SUCCESS(f'✓ {fixture_name} cargado correctamente'))
            except Exception as e:
                has_errors = True
                self.stdout.write(self.style.ERROR(f'× Error al cargar {fixture_name}: {str(e)}'))

        if has_errors:
            self.stdout.write(self.style.ERROR('=== SEEDS TERMINADOS CON ERRORES ==='))
        else:
            self.stdout.write(self.style.SUCCESS('=== SEEDS CARGADOS CORRECTAMENTE ==='))
            self.show_summary()

    def load_fixture(self, fixture_name, model_class):
        fixture_path = Path(f'core/fixtures/{fixture_name}.json')
        with open(fixture_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        now = timezone.now()
        objects = []
        
        for item in data:
            fields = item.get('fields', {}).copy()
            
            # UUID automático asignado dinámicamente
            if hasattr(model_class, 'external_id'):
                fields['external_id'] = uuid.uuid4()
            # created_at automático
            if hasattr(model_class, 'created_at'):
                fields['created_at'] = now
            # updated_at automático
            if hasattr(model_class, 'updated_at'):
                fields['updated_at'] = now
                
            obj = model_class(**fields)
            objects.append(obj)
            
        # SQL Server no soporta ignore_conflicts, se usa bulk_create directo
        model_class.objects.bulk_create(objects)

    def clear_all_catalogs(self):
        self.stdout.write(self.style.WARNING('=== LIMPIANDO DATOS ==='))
        Skill.objects.all().delete()
        Languages.objects.all().delete()
        JobTitle.objects.all().delete()
        Degrees.objects.all().delete()
        AcademicField.objects.all().delete()
        
        with connection.cursor() as cursor:
            for table in self.TABLES:
                try:
                    cursor.execute(f"DBCC CHECKIDENT ('{table}', RESEED, 0)")
                except Exception:
                    pass
        self.stdout.write(self.style.SUCCESS('✓ Datos eliminados correctamente'))

    def show_summary(self):
        self.stdout.write('\n--- RESUMEN ---')
        self.stdout.write(f'Academic Fields: {AcademicField.objects.count()}')
        self.stdout.write(f'Degrees: {Degrees.objects.count()}')
        self.stdout.write(f'Job Titles: {JobTitle.objects.count()}')
        self.stdout.write(f'Languages: {Languages.objects.count()}')
        self.stdout.write(f'Skills: {Skill.objects.count()}')
        
        self.stdout.write('\n=== UUIDs GENERADOS ===')
        af = AcademicField.objects.first()
        if af:
            self.stdout.write(f'AcademicField UUID: {af.external_id}')
        job = JobTitle.objects.first()
        if job:
            self.stdout.write(f'JobTitle UUID: {job.external_id}')
        lang = Languages.objects.first()
        if lang:
            self.stdout.write(f'Languages UUID: {lang.external_id}')
        skill = Skill.objects.first()
        if skill:
            self.stdout.write(f'Skill UUID: {skill.external_id}')
        self.stdout.write('-------------------------')