# from django.core.management.base import BaseCommand
# from user_management.models import Role
#
#
# class Command(BaseCommand):
#     help = 'Populate the database with predefined roles'
#
#     def handle(self, *args, **kwargs):
#         ROLE_GROUPS = {
#             'Family': [
#                 ('Father', 'Father'),
#                 ('Mother', 'Mother'),
#                 ('Husband', 'Husband'),
#                 ('Wife', 'Wife'),
#                 ('Son', 'Son'),
#                 ('Daughter', 'Daughter'),
#                 ('Brother', 'Brother'),
#                 ('Sister', 'Sister'),
#                 ('Partner', 'Partner')
#             ],
#             'Professional': [
#                 ('Colleague', 'Colleague'),
#                 ('Mentor', 'Mentor'),
#                 ('Mentee', 'Mentee'),
#                 ('Leader', 'Leader'),
#                 ('Planner', 'Planner'),
#                 ('Collaborator', 'Collaborator'),
#                 ('Communicator', 'Communicator'),
#                 ('Learner', 'Learner'),
#             ],
#             'Other': [
#                 ('Friend', 'Friend'),
#                 ('Other', 'Other'),
#             ]
#         }
#
#         for group, roles in ROLE_GROUPS.items():
#             for role_name, role_display in roles:
#                 Role.objects.get_or_create(role_name=role_name, role_group=group)
#         self.stdout.write(self.style.SUCCESS('Successfully populated the roles.'))
