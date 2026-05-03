import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None: 
    raise Exception("API Key not found!")

#parse CLI arguments using builtin
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

#Import the genai library and use the API key to create a new instance of a Gemini client:
client = genai.Client(api_key=api_key)

response_object = client.models.generate_content(model='gemini-2.5-flash',contents=messages)

if response_object.usage_metadata == None:
    raise Exception("Usage metrics returned None!")

#Print token usage to the screen
if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response_object.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response_object.usage_metadata.candidates_token_count}")

print(response_object.text)