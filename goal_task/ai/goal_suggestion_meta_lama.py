# import logging
#
# from azure.ai.inference import ChatCompletionsClient
# from azure.ai.inference.models import SystemMessage, UserMessage
# from azure.core.credentials import AzureKeyCredential
#
# # Define the endpoint and model name
# endpoint = "https://models.inference.ai.azure.com"
# model_name = "Meta-Llama-3.1-405B-Instruct"
# token = "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"
#
# # Initialize the client with AzureKeyCredential
# client = ChatCompletionsClient(
#     endpoint=endpoint,
#     credential=AzureKeyCredential(token),
# )
#
#
# def generate_goal_with_meta_llama(user_profile, selected_role):
#     try:
#         # Prepare user data
#         age = user_profile.get_age()
#         gender = {"M": "male", "F": "female", "O": "other"}.get(
#             user_profile.gender, "prefer not to say"
#         )
#
#         # Define the instructions and user profile for goal generation
#         instructions = """
#         1. Goal Title and Description:
#             • Generate 25 unique goals with a concise title and description.
#             • Format each goal as follows:
#                 {
#                     "title": "[Goal Number]. **Title:** \"[Goal Title]\"",
#                     "description": "**Description:** [Goal Description]"
#                 }
#         2. Personalization Criteria:
#             • The goal must be tailored to the user’s role, age, and sex.
#         3. Focus on One Function:
#             • Ensure each goal is related to only one specific aspect or function. The goal should not cover multiple areas but rather focus on a single, clearly defined objective.
#         """
#
#         # Construct the prompt based on user profile
#         prompt = f"{instructions}\n\nUser Profile: {gender.capitalize()}, {age} years old, Role: {selected_role}\n"
#
#         # Send the request to Meta-Llama via Azure
#         response = client.complete(
#             messages=[
#                 SystemMessage(content="You are a helpful assistant."),
#                 UserMessage(content=prompt),
#             ],
#             temperature=1.0,  # Adjust temperature if needed
#             top_p=1.0,  # Adjust top_p value for randomness control
#             max_tokens=1000,  # Set the token limit for the response
#             model=model_name  # Meta-Llama model name
#         )
#
#         # Extract the generated content from the response
#         generated_goals_text = response.choices[0].message.content
#
#         # Parse the generated goals into title and description
#         generated_goals = []
#         for goal in generated_goals_text.split("\n\n"):
#             try:
#                 goal_dict = eval(goal)
#                 title = goal_dict["title"].split(": ", 1)[-1].strip().replace('"', '')
#                 description = goal_dict["description"].split(": ", 1)[-1].strip()
#                 generated_goals.append({
#                     "title": title,
#                     "description": description
#                 })
#             except Exception as e:
#                 logging.warning(f"Error parsing goal: {e}")
#
#         return generated_goals
#
#     except Exception as e:
#         logging.error(f"Error generating goals: {e}")
#         return []
