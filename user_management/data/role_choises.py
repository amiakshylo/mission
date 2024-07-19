ROLE_GROUPS = {
        'Family': [
            ('Father', 'Father'),
            ('Mother', 'Mother'),
            ('Husband', 'Husband'),
            ('Wife', 'Wife'),
            ('Son', 'Son'),
            ('Daughter', 'Daughter'),
            ('Brother', 'Brother'),
            ('Sister', 'Sister'),
            ('Partner', 'Partner')
        ],
        'Professional': [
            ('Colleague', 'Colleague'),
            ('Mentor', 'Mentor'),
            ('Mentee', 'Mentee'),
            ('Leader', 'Leader'),
            ('Planner', 'Planner'),
            ('Collaborator', 'Collaborator'),
            ('Communicator', 'Communicator'),
            ('Learner', 'Learner'),
        ],
        'Other': [
            ('Friend', 'Friend'),
            ('Other', 'Other'),
        ]
    }

ROLE_CHOICES = [(role, name) for group in ROLE_GROUPS.values() for role, name in group]