import json
from django.core.management.base import BaseCommand
from user_management.models import PredefinedGoal


class Command(BaseCommand):
    help = 'Load data from predefined_goals.json ensuring unique titles'

    def handle(self, *args, **kwargs):
        with open('user_management/data/predefined_goals.json', 'r') as file:
            data = json.load(file)

        for item in data:
            title = item['fields']['title']
            description = item['fields']['description']
            type = item['fields']['type']

            if not PredefinedGoal.objects.filter(title=title).exists():
                PredefinedGoal.objects.create(
                    title=title,
                    description=description,
                    type=type
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded data ensuring unique titles'))