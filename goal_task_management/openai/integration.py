import os
from openai import OpenAI

from goal_task_management.models import Goal


def generate_goal_with_openai(user_profile, selected_role):
    """
    This function sends a request to the OpenAI API to generate a goal based on the user's profile and the selected role.

    Args:
        user_profile (UserProfile): The user's profile, containing information like age, etc.
        selected_role (str): The specific role selected by the user.

    Returns:
        list: A list of dictionaries, each containing 'title' and 'description' of the generated goals.
    """

    # Fetch the user's age directly
    age = user_profile.get_age()

    # Convert gender code to descriptive string
    gender = {
        'M': "male",
        'F': "female",
        'O': "non-binary"
    }.get(user_profile.gender, "prefer not to say")

    # Instructions for AI
    instructions = """
    You are an AI assistant that generates a list of goals based on the user's role, sex, and age. Your task is to provide concise, specific, and actionable goals without using any special formatting like asterisks, bold text, or additional emphasis. Keep each goal's description brief, direct, and relevant.

    1. Role: Tailor goals to the user's selected role, focusing on practical advice and actionable steps.

    2. Sex: Consider the user's gender where it impacts the goal, but focus on universal and practical advice.

    3. Age: Adjust goals based on the user's age, considering their life stage.

    4. Output: Present each goal with a clear title and a brief, straightforward description. Avoid any special formatting like asterisks or bold text. Keep descriptions concise, typically no more than one short sentence.

    Ensure the response is concise, without special formatting, and with clear, brief descriptions. Now, suggest a list of goals based on the user's role, sex, and age.
    """

    # Combine the user's data with the instructions to create the full prompt
    prompt = f"{instructions}\n\nUser Profile: {gender.capitalize()}, {age} years old, Role: {selected_role}\n"

    try:
        # Initialize the OpenAI client
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Send request to OpenAI using the updated ChatCompletion interface
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or use "gpt-4" or other available models
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": prompt}
            ]
        )

        # Correctly access the message content
        generated_goals_text = chat_completion.choices[0].message.content.strip()

        # Split the generated text into individual goals
        goals = generated_goals_text.split("\n\n")
        parsed_goals = []

        for goal in goals:
            if goal.strip():  # Ensure there's content
                parts = goal.split(": ", 1)
                if len(parts) == 2:
                    title = parts[0].strip()
                    description = parts[1].strip()
                    parsed_goals.append({'title': title, 'description': description})

        return parsed_goals

    except Exception as e:
        print(f"OpenAI API request failed: {e}")
        return []


def save_generated_goals(user_profile, generated_goals):
    """
    Save each generated goal into the database.
    """
    for goal in generated_goals:
        goal_instance = Goal.objects.create(
            title=goal['title'],
            description=goal['description'],
            is_custom=True,  # Marking it as custom since it was generated
            created_by=user_profile.user,
        )
        GoalSuggestionLog.objects.create(user_profile=user_profile, goal=goal_instance, suggestion_source='openai')
        UserGoal.objects.create(user_profile=user_profile, goal=goal_instance)