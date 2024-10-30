import json
import logging
import os
from typing import TypedDict

from openai import OpenAI


class Goal(TypedDict):
    title: str
    description: str


def generate_goal_with_openai(user_profile, selected_role):
    """
    This function sends a request to the OpenAI API to generate a goal
    based on the user's profile and the selected role.
    """
    try:
        # Retrieve user's age and gender
        age = user_profile.get_age()
        gender = {"M": "male", "F": "female", "O": "other"}.get(
            user_profile.gender, "prefer not to say"
        )

        instructions = """
                        1. Goal Title and Description:
                            • Generate 2 goals with a concise title and description.
                            • Return it in JSON format where goals its a list od dictionary with key value pair title
                            and description
                            • Do **not** include additional text, explanations, or formatting beyond the JSON object.
                        2. Personalization Criteria:
                            • The goal must be tailored to the user’s role, age, and sex.
                        3. Focus on One Function:
                            • Ensure each goal is related to only one specific aspect or function.
                              The goal should not cover multiple areas but rather focus on a 
                              single, clearly defined objective.
                        """

        # Create a prompt for OpenAI based on user profile
        prompt = f"{instructions}\n\nUser Profile: {gender.capitalize()}, {age} years old, Role: {selected_role}\n"

        # Initialize OpenAI client with the API key
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Call OpenAI API to get the chat completion response
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"}
        )

        # Get the generated content from the API response
        response = chat_completion.choices[0].message.content
        print(type(response))

        response_json = json.loads(response)
        print(response_json)

        return response_json

    except Exception as e:
        logging.error(f"Error generating goals: {e}")
        return []
