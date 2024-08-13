import csv

from django.core.management.base import BaseCommand

from goal_task_management.models import Goal
from user_management.models import UserRole


class Command(BaseCommand):
    help = 'Populate the many-to-many relationship between Goal and UserRole from CSV'

    def handle(self, *args, **kwargs):
        csv_file_path = '/Users/andrewdev/PycharmProjects/7habits/!!!goals.csv'  # Update with your actual file path

        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    goal_id = int(row['id'])  # Assuming 'id' is the goal_id in your CSV
                    role_ids = [int(role_id) for role_id in
                                row['role_id'].split(',')]  # Assuming comma-separated role_ids

                    # Fetch the Goal instance
                    goal = Goal.objects.get(id=goal_id)

                    # Add each role to the goal
                    for role_id in role_ids:
                        role = UserRole.objects.get(id=role_id)
                        goal.user_role.add(role)

                    goal.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully added roles to Goal ID {goal_id}'))

                except Goal.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Goal with ID "{goal_id}" does not exist'))
                except UserRole.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'UserRole with ID {role_id} does not exist'))

        self.stdout.write(self.style.SUCCESS('Finished populating the Goal-UserRole relationship'))