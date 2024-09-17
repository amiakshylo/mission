# services.py or utils.py
from life_sphere.models import LifeSphere
from onboarding.utils import calculate_total_points_per_life_sphere
from .models import UserBalance


def save_initial_user_balance(user_profile):
    life_sphere_points = calculate_total_points_per_life_sphere(user_profile)

    # Loop through each life sphere and save the balance
    for life_sphere_title, points in life_sphere_points.items():
        # Get the LifeSphere object based on its name or other key
        life_sphere = LifeSphere.objects.get(title=life_sphere_title)

        # Use get_or_create to avoid duplicating records
        UserBalance.objects.get_or_create(
            user_profile=user_profile,
            life_sphere=life_sphere,
            defaults={"score": points},
        )
