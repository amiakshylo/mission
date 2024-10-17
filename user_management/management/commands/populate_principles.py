from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from core.model_choices import GenderChoices
from principle.models import Principle, RoleModel
from user_management.models import UserProfile


class Command(BaseCommand):
    help = 'Populate the database with predefined Principles and RoleModels'

    def handle(self, *args, **options):
        try:
            self.stdout.write('Starting data population...')
            self.populate_principles()
            self.populate_role_models()
            self.stdout.write(self.style.SUCCESS('Data population completed successfully!'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))

    def get_system_user_profile(self):
        # Adjust the username to match your system user
        system_username = 'system_user'  # Replace with your system user's username

        try:
            system_user = User.objects.get(username=system_username)
            system_user_profile = UserProfile.objects.get(user=system_user)
            return system_user_profile
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'User "{system_username}" does not exist.'))
            exit(1)
        except UserProfile.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'UserProfile for "{system_username}" does not exist.'))
            exit(1)

    def populate_principles(self):
        self.stdout.write('Populating Principles...')
        principles_data = [
            {'title': 'Courage', 'description': 'Facing fears and challenges with bravery.'},
            {'title': 'Justice', 'description': 'Promoting fairness and equity.'},
            {'title': 'Perseverance', 'description': 'Persisting in spite of difficulties.'},
            {'title': 'Innovation', 'description': 'Thinking creatively to solve problems.'},
            {'title': 'Compassion', 'description': 'Showing kindness and empathy towards others.'},
            {'title': 'Integrity', 'description': 'Being honest and having strong moral principles.'},
            {'title': 'Leadership', 'description': 'Guiding others towards a common goal.'},
            {'title': 'Humility', 'description': 'Being modest and respectful.'},
            {'title': 'Wisdom', 'description': 'Applying knowledge and experience with good judgment.'},
            {'title': 'Resilience', 'description': 'Recovering quickly from setbacks.'},
            {'title': 'Service', 'description': 'Contributing to the welfare of others.'},
            {'title': 'Education', 'description': 'Valuing knowledge and learning.'},
            {'title': 'Creativity', 'description': 'Expressing originality and imagination.'},
            {'title': 'Authenticity', 'description': 'Being true to oneself.'},
            {'title': 'Non-violence', 'description': 'Promoting peaceful resolution of conflicts.'},
            {'title': 'Curiosity', 'description': 'Desire to learn and discover new things.'},
            {'title': 'Independence', 'description': 'Self-reliance and freedom from external control.'},
            {'title': 'Environmentalism', 'description': 'Advocating for the protection of the environment.'},
            {'title': 'Advocacy', 'description': 'Actively supporting a cause or proposal.'},
            {'title': 'Exploration', 'description': 'Pursuing discovery in unknown areas.'},
            {'title': 'Vision', 'description': 'Having a clear idea about what you want to achieve.'},
            {'title': 'Pioneering', 'description': 'Being among the first to explore or develop something new.'},
        ]

        system_user_profile = UserProfile.objects.get(id=2)

        for principle_data in principles_data:
            principle, created = Principle.objects.get_or_create(
                title=principle_data['title'],
                defaults={
                    'description': principle_data['description'],
                    'created_by': system_user_profile,
                    'is_predefined': True,
                }
            )
            if created:
                self.stdout.write(f'Created Principle: {principle.title}')
            else:
                self.stdout.write(f'Principle already exists: {principle.title}')

    def populate_role_models(self):
        self.stdout.write('Populating RoleModels...')
        role_models_data = [
            # Include all 20 role models as defined earlier
            {
                'character_name': 'Nelson Mandela',
                'description': 'Anti-apartheid revolutionary and former President of South Africa.',
                'gender': GenderChoices.MAIL,
                'principles': ['Courage', 'Justice', 'Perseverance'],
            },
            {
                'character_name': 'Marie Curie',
                'description': 'Pioneering physicist and chemist who conducted groundbreaking research on radioactivity.',
                'gender': GenderChoices.FEMAIL,
                'principles': ['Innovation', 'Perseverance', 'Humility'],
            },
            {
                'character_name': 'Mahatma Gandhi',
                'description': 'Leader of the Indian independence movement known for his philosophy of non-violent civil disobedience.',
                'gender': GenderChoices.MAIL,
                'principles': ['Non-violence', 'Integrity', 'Compassion'],
            },
            {
                'character_name': 'Mother Teresa',
                'description': 'Catholic nun and missionary who dedicated her life to helping the poor and sick.',
                'gender': GenderChoices.FEMAIL,
                'principles': ['Compassion', 'Service', 'Humility'],
            },
            {
                'character_name': 'Albert Einstein',
                'description': 'Theoretical physicist who developed the theory of relativity.',
                'gender': GenderChoices.MAIL,
                'principles': ['Curiosity', 'Innovation', 'Humility'],
            },
            {
                'character_name': 'Rosa Parks',
                'description': 'Civil rights activist known for her pivotal role in the Montgomery bus boycott.',
                'gender': GenderChoices.FEMAIL,
                'principles': ['Courage', 'Justice', 'Perseverance'],
            },
            {
                'character_name': 'Martin Luther King Jr.',
                'description': 'Leader of the American civil rights movement advocating for equality through non-violent means.',
                'gender': GenderChoices.MAIL,
                'principles': ['Justice', 'Leadership', 'Integrity'],
            },
            {
                'character_name': 'Amelia Earhart',
                'description': 'Aviation pioneer and author, the first female aviator to fly solo across the Atlantic Ocean.',
                'gender': GenderChoices.FEMAIL,
                'principles': ['Courage', 'Perseverance', 'Independence'],
            },
            {
                'character_name': 'Leonardo da Vinci',
                'description': 'Renaissance artist, inventor, and polymath known for works like the Mona Lisa.',
                'gender': GenderChoices.MAIL,
                'principles': ['Creativity', 'Innovation', 'Curiosity'],
            },
            {
                'character_name': 'Malala Yousafzai',
                'description': 'Youngest Nobel Prize laureate advocating for girls\' education.',
                'gender': GenderChoices.FEMAIL,
                'principles': ['Courage', 'Education', 'Justice'],
            },
            {
                'character_name': 'Abraham Lincoln',
                'description': '16th President of the United States who led the nation through the Civil War.',
                'gender': GenderChoices.MAIL,
                'principles': ['Integrity', 'Leadership', 'Justice'],
            },
            {
                'character_name': 'Florence Nightingale',
                'description': 'Founder of modern nursing who improved sanitary conditions in medical facilities.',
                'gender': GenderChoices.FEMAIL,
                'principles': ['Compassion', 'Service', 'Perseverance'],
            },
            {
                'character_name': 'Steve Jobs',
                'description': 'Co-founder of Apple Inc., known for his role in the personal computer revolution.',
                'gender': GenderChoices.MAIL,
                'principles': ['Innovation', 'Vision', 'Perseverance'],
            },
            {
                'character_name': 'Ada Lovelace',
                'description': 'Mathematician considered to be the world\'s first computer programmer.',
                'gender': GenderChoices.FEMAIL,
                'principles': ['Innovation', 'Pioneering', 'Perseverance'],
            },
            {
                'character_name': 'Winston Churchill',
                'description': 'Former Prime Minister of the UK who led the country during World War II.',
                'gender': GenderChoices.MAIL,
                'principles': ['Leadership', 'Courage', 'Resilience'],
            },
            {
                'character_name': 'Jane Goodall',
                'description': 'Primatologist and anthropologist known for her study of wild chimpanzees.',
                'gender': GenderChoices.FEMAIL,
                'principles': ['Compassion', 'Environmentalism', 'Perseverance'],
            },
            {
                'character_name': 'Frida Kahlo',
                'description': 'Mexican artist known for her self-portraits and works inspired by nature and Mexican culture.',
                'gender': GenderChoices.MAIL,
                'principles': ['Creativity', 'Authenticity', 'Resilience'],
            },
            {
                'character_name': 'Thomas Edison',
                'description': 'Inventor and businessman who developed many devices, including the phonograph and the electric light bulb.',
                'gender': GenderChoices.MAIL,
                'principles': ['Innovation', 'Perseverance', 'Resilience'],
            },
            {
                'character_name': 'Eleanor Roosevelt',
                'description': 'Former First Lady of the United States and human rights activist.',
                'gender': GenderChoices.FEMAIL,
                'principles': ['Leadership', 'Compassion', 'Advocacy'],
            },
            {
                'character_name': 'Neil Armstrong',
                'description': 'Astronaut and aeronautical engineer, first person to walk on the Moon.',
                'gender': GenderChoices.MAIL,
                'principles': ['Courage', 'Exploration', 'Perseverance'],
            },
        ]

        # Map principle titles to Principle instances
        principle_map = {principle.title: principle for principle in Principle.objects.all()}

        with transaction.atomic():
            for role_model_data in role_models_data:
                character_name = role_model_data['character_name']
                description = role_model_data['description']
                gender = role_model_data['gender']
                principle_titles = role_model_data['principles']

                # Validate gender
                gender_choices = [choice[0] for choice in GenderChoices.GENDER_TYPE_CHOICES]
                if gender not in gender_choices:
                    self.stderr.write(f'Invalid gender "{gender}" for "{character_name}". Skipping.')
                    continue

                role_model, created = RoleModel.objects.get_or_create(
                    character_name=character_name,
                    defaults={
                        'description': description,
                        'gender': gender,
                    }
                )

                if created:
                    self.stdout.write(f'Created RoleModel: {role_model.character_name}')
                else:
                    self.stdout.write(f'RoleModel already exists: {role_model.character_name}')

                # Get Principle instances
                principles = []
                for title in principle_titles:
                    principle = principle_map.get(title)
                    if principle:
                        principles.append(principle)
                    else:
                        self.stderr.write(
                            f'Principle "{title}" not found for "{character_name}". Skipping this principle.')

                # Associate principles with the role model
                role_model.principle.set(principles)  # Replace existing associations
                # Alternatively, use role_model.principle.add(*principles) to add without overwriting
