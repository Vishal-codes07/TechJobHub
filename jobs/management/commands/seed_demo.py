from django.core.management.base import BaseCommand

from accounts.models import CustomUser
from jobs.models import Job

DEMO_PASSWORD = 'Demo@12345'

JOBS = [
    ('Python Django Developer', 'Nexora Technologies', 'Gurugram, Haryana', 720000,
     'We are looking for a Django developer to build and maintain internal tools and customer-facing APIs.\n\n'
     'What you will do:\n- Build REST APIs with Django and DRF\n- Write clean, tested code\n- Work with the product team on new features\n\n'
     'What we need:\n- 1+ years of Python and Django\n- Good SQL basics\n- Git knowledge'),
    ('Frontend Developer (React)', 'PixelCraft Studio', 'Bengaluru, Karnataka', 900000,
     'Join our design-led team to build fast, accessible interfaces in React.\n\n'
     'You should know HTML, CSS, modern JavaScript and have shipped at least one real project.'),
    ('Digital Marketing Executive', 'GrowthLoop Media', 'Delhi', 360000,
     'Plan and run SEO, social and email campaigns for our clients.\n\n'
     'Good written English, basic analytics skills and a curious mind are what matter most.'),
    ('Data Analyst', 'Insightly Analytics', 'Hyderabad, Telangana', 600000,
     'Turn raw data into clear dashboards and reports for business teams.\n\n'
     'Skills: SQL, Excel, Python (pandas) and any BI tool such as Power BI or Tableau.'),
    ('Customer Support Associate', 'HelpHive Services', 'Noida, Uttar Pradesh', 280000,
     'Handle customer queries over chat and email, and keep our response quality high.\n\n'
     'Freshers are welcome. Training is provided and rotational shifts apply.'),
    ('HR Recruiter', 'TalentBridge Consulting', 'Pune, Maharashtra', 420000,
     'Source, screen and coordinate interviews for IT and non-IT roles.\n\n'
     'Prior experience with job portals and LinkedIn sourcing is a plus.'),
    ('Mobile App Developer (Flutter)', 'Zippy Apps', 'Rohtak, Haryana', 540000,
     'Build and ship cross-platform apps in Flutter for Android and iOS.\n\n'
     'We would like to see a Play Store or GitHub portfolio.'),
    ('Accounts Executive', 'Sharma & Associates', 'Chandigarh', 300000,
     'Maintain books, handle GST filings and support the audit team.\n\n'
     'B.Com degree and working knowledge of Tally are required.'),
]


class Command(BaseCommand):
    help = 'Create demo users and sample jobs (safe to run more than once).'

    def handle(self, *args, **options):
        admin, created = CustomUser.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True, 'role': 'employer'},
        )
        if created:
            admin.set_password('Admin@12345')
            admin.save()

        employer, created = CustomUser.objects.get_or_create(
            username='employer1', defaults={'email': 'employer1@example.com', 'role': 'employer'}
        )
        if created:
            employer.set_password(DEMO_PASSWORD)
            employer.save()

        seeker, created = CustomUser.objects.get_or_create(
            username='seeker1', defaults={'email': 'seeker1@example.com', 'role': 'seeker'}
        )
        if created:
            seeker.set_password(DEMO_PASSWORD)
            seeker.save()

        added = 0
        for title, company, location, salary, description in JOBS:
            _, was_created = Job.objects.get_or_create(
                title=title, company_name=company,
                defaults={'location': location, 'salary': salary, 'description': description, 'posted_by': employer},
            )
            added += was_created

        self.stdout.write(self.style.SUCCESS(f'Demo data ready ({added} new jobs).'))
        self.stdout.write('  admin     / Admin@12345  (admin panel at /admin/)')
        self.stdout.write(f'  employer1 / {DEMO_PASSWORD}')
        self.stdout.write(f'  seeker1   / {DEMO_PASSWORD}')
