# from dotenv import load_dotenv
# import os
# from openai import OpenAI
#
#
# load_dotenv()
#
# print("API Key:", os.getenv("OPENAI_API_KEY"))
#
# def test_openai_connection():
#     api_key = os.getenv("OPENAI_API_KEY")
#     print("API Key:", api_key)
#
#     try:
#         # Initialize the OpenAI client with the api_key variable
#         client = OpenAI(
#             api_key=api_key,
#         )
#
#         # Create a chat completion request
#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "user",
#                     "content": "Say this is a test",
#                 }
#             ],
#             model="gpt-3.5-turbo",
#         )
#
#         # Correct way to access the content of the response
#         response_message = chat_completion.choices[0].message.content.strip()
#         print("OpenAI connected. Response:", response_message)
#
#     except Exception as e:
#         print("Error connecting to OpenAI:", e)