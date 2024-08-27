
import os
from openai import OpenAI



def generate_goal_with_openai(user_profile, selected_role):
    """
    This function sends a request to the OpenAI API to generate a goal based on the user's profile and the selected role.
    """

    age = user_profile.get_age()

    gender = {
        'M': "male",
        'F': "female",
        'O': "other"
    }.get(user_profile.gender, "prefer not to say")

    instructions = """
    1. Goal Title and Description:
        • Generate a 50 unique goals with a concise title.
        • Provide a straightforward description within one short sentence.
    2. Personalization Criteria:
        • The goal must be tailored to the user’s role, age, and sex.
    3. Focus on One Function:
        • Ensure each goal is related to only one specific aspect or function. The goal should not cover multiple areas but rather focus on a single, clearly defined objective.
    4. Example Format:
        • Title: [Goal Title]
        • Description: [One-sentence goal description]

    """

    prompt = f"{instructions}\n\nUser Profile: {gender.capitalize()}, {age} years old, Role: {selected_role}\n"


    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": prompt}
        ],

    )
    response = chat_completion.choices[0].message.content

    # Correctly access the content
    generated_goals = []
    for goal in response.split("\n\n"):
        # Ensure that the split only returns exactly two parts
        parts = goal.split("\n", 1)
        if len(parts) == 2:
            title_line, description_line = parts
            title = title_line.split(": ", 1)[-1].strip()  # Safely handle splitting
            description = description_line.split(": ", 1)[-1].strip()
            generated_goals.append({
                'title': title,
                'description': description
            })
        else:
            print(f"Unexpected goal format: {goal}")
    return generated_goals

