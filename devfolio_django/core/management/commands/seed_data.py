from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from core.models import Category, Project, Review, Technology


class Command(BaseCommand):
    help = 'Seed the DevFolio app with demo categories, technologies, users, and projects.'

    def handle(self, *args, **options):
        User = get_user_model()

        categories = [
            'Web Development',
            'Mobile Development',
            'Artificial Intelligence',
            'Database Systems',
            'Game Development',
            'IoT',
        ]

        technologies = [
            'Django', 'Python', 'PHP', 'Laravel', 'JavaScript',
            'React', 'Flutter', 'Java', 'MySQL', 'Firebase',
            'TensorFlow', 'Node.js', 'C#', 'Unity', 'Arduino'
        ]

        category_objs = []
        for name in categories:
            category, created = Category.objects.get_or_create(name=name)
            category_objs.append(category)

        tech_objs = []
        for name in technologies:
            tech, created = Technology.objects.get_or_create(name=name)
            tech_objs.append(tech)

        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@devfolio.test',
                'role': User.ROLE_ADMIN,
                'is_staff': True,
                'is_superuser': True,
                'full_name': 'System Admin',
            }
        )
        if created:
            admin_user.set_password('admin123')
        admin_user.email_verified = True
        admin_user.is_active = True
        admin_user.save()

        moderator_user, created = User.objects.get_or_create(
            username='moderator',
            defaults={
                'email': 'moderator@devfolio.test',
                'role': User.ROLE_MODERATOR,
                'is_staff': True,
                'full_name': 'Project Moderator',
                'course': 'Information Technology',
            }
        )
        if created:
            moderator_user.set_password('moderator123')
        moderator_user.email_verified = True
        moderator_user.is_active = True
        moderator_user.save()

        for i in range(1, 4):
            username = f'student{i}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'student{i}@devfolio.test',
                    'role': User.ROLE_STUDENT,
                    'full_name': f'Student {i}',
                    'course': 'Computer Science',
                    'year_level': 3,
                }
            )
            if created:
                user.set_password('student123')
            user.email_verified = True
            user.is_active = True
            user.save()

        project_data = [
            {
                'title': 'Campus Event Planner',
                'summary': 'A web app for scheduling events and managing event participation.',
                'description': 'This project streamlines event announcements, registration, and schedule tracking for campus activities.',
                'owner': 'student1',
                'category': 'Web Development',
                'status': Project.STATUS_APPROVED,
                'techs': ['Django', 'Python', 'JavaScript'],
            },
            {
                'title': 'Smart Attendance Tracker',
                'summary': 'A mobile and web-based attendance tracking app for classrooms.',
                'description': 'The app provides quick attendance recording, class analytics, and secure student records.',
                'owner': 'student2',
                'category': 'Mobile Development',
                'status': Project.STATUS_UNDER_REVIEW,
                'techs': ['Flutter', 'Firebase', 'Python'],
            },
            {
                'title': 'AI Course Recommender',
                'summary': 'An intelligent system that suggests courses to students based on interests and grades.',
                'description': 'This application uses a rule-based recommendation engine and analysis dashboard for academic guidance.',
                'owner': 'student3',
                'category': 'Artificial Intelligence',
                'status': Project.STATUS_APPROVED,
                'techs': ['Python', 'TensorFlow', 'React'],
            },
            {
                'title': 'Inventory Control System',
                'summary': 'A system for tracking products, sales, and inventory levels in stores.',
                'description': 'This project helps business owners manage stock movement and record low inventory alerts.',
                'owner': 'student1',
                'category': 'Database Systems',
                'status': Project.STATUS_APPROVED,
                'techs': ['PHP', 'Laravel', 'MySQL'],
            },
            {
                'title': 'Smart Irrigation Monitor',
                'summary': 'An IoT application that monitors moisture and automates watering schedules.',
                'description': 'The project tracks soil conditions and sends alerts to users for smart and efficient irrigation.',
                'owner': 'student2',
                'category': 'IoT',
                'status': Project.STATUS_REJECTED,
                'techs': ['Arduino', 'Python', 'C#'],
            },
        ]

        for data in project_data:
            owner = User.objects.get(username=data['owner'])
            category = Category.objects.get(name=data['category'])
            project, created = Project.objects.get_or_create(
                title=data['title'],
                defaults={
                    'owner': owner,
                    'category': category,
                    'summary': data['summary'],
                    'description': data['description'],
                    'status': data['status'],
                }
            )
            project.technologies.set(Technology.objects.filter(name__in=data['techs']))

        review_data = [
            ('student1', 'Campus Event Planner', 5, 'Very useful and well structured.'),
            ('student2', 'Campus Event Planner', 4, 'Great features and clean user experience.'),
            ('student3', 'AI Course Recommender', 5, 'Helpful and practical for students.'),
        ]

        for username, title, rating, comment in review_data:
            reviewer = User.objects.get(username=username)
            project = Project.objects.get(title=title)
            Review.objects.get_or_create(
                project=project,
                reviewer=reviewer,
                defaults={'rating': rating, 'comment': comment},
            )

        self.stdout.write(self.style.SUCCESS('Seed data created successfully.'))
