import csv
from django.core.management.base import BaseCommand
from goal_task_management.models import Goal
from user_management.models import Role


class Command(BaseCommand):
    help = 'Populate database with goals from a CSV file'

    def handle(self, *args, **kwargs):
        file_path = '/Users/andrewdev/PycharmProjects/7habits/user_management/data/!!!goals.csv'

        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Assuming role_id exists in your database
                role = Role.objects.get(id=row['role_ids'])
                goal = Goal(
                    title=row['title'],
                    description=row['description'],
                    is_custom=row['is_custom'] == 'True',
                    impact_score=int(row['impact_score']),
                    goal_type=row['goal_type'],
                )
                goal.save()
                goal.role.add(role)
                self.stdout.write(self.style.SUCCESS(f'Successfully added goal: {row["title"]}'))

        self.stdout.write(self.style.SUCCESS('Database population complete!'))
