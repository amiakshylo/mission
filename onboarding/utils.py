from .models import UserResponse


def calculate_total_points_per_life_sphere(user_profile):
    life_sphere_points = {}

    user_responses = (
        UserResponse.objects.filter(user_profile=user_profile)
        .select_related("question__life_sphere")
        .select_related("user_answer")
    )

    for response in user_responses:
        life_sphere = response.question.life_sphere
        life_sphere_key = life_sphere.title

        if life_sphere_key not in life_sphere_points:
            life_sphere_points[life_sphere_key] = 0

        life_sphere_points[life_sphere_key] += response.calculate_points()

    return life_sphere_points
