from django.core.management.base import BaseCommand
from user_management.models import PredefinedRole, PredefinedGoal
from user_management.data import goal_chooses, role_chooses


class Command(BaseCommand):
    help = 'Populates the database with predefined roles and goals'

    def handle(self, *args, **kwargs):
        self.populate_roles()
        self.populate_goals()
        self.link_roles_goals()
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with predefined roles and goals'))

    def populate_roles(self):
        for role_title, goals in role_choises.ROLE_GROUPS.items():
            role, created = PredefinedRole.objects.get_or_create(title=role_title)
            if created:
                self.stdout.write(f'Created role: {role_title}')

    def populate_goals(self):
        for role_title, goals in goal_chooses.ROLE_GOAL_CHOICES.items():
            for goal_data in goals:
                goal_code, goal_title, goal_type = goal_data
                goal, created = PredefinedGoal.objects.get_or_create(title=goal_title, defaults={'type': goal_type})
                if created:
                    self.stdout.write(f'Created goal: {goal_title}')

    def link_roles_goals(self):
        for role_title, goals in goal_chooses.ROLE_GOAL_CHOICES.items():
            role = PredefinedRole.objects.get(title=role_title)
            for goal_data in goals:
                goal_code, goal_title, _ = goal_data
                goal = PredefinedGoal.objects.get(title=goal_title)
                role.goal.add(goal)
            self.stdout.write(f'Linked {role_title} with its goals')
