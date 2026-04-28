import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None: 
    raise Exception("API Key not found!")

#Import the genai library and use the API key to create a new instance of a Gemini client:
client = genai.Client(api_key=api_key)

response_object = client.models.generate_content(model='gemini-2.5-flash',contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")

if response_object.usage_metadata == None:
    raise Exception("Usage metrics returned None!")

#Print token usage to the screen
print(f"Prompt tokens: {response_object.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response_object.usage_metadata.candidates_token_count}")

print(response_object.text)