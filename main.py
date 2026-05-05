import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from sys import exit
from functions.call_function import available_functions
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None: 
    raise Exception("API Key not found!")

#parse CLI arguments using builtin
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

#Import the genai library and use the API key to create a new instance of a Gemini client:
client = genai.Client(api_key=api_key)

for _ in range(20):

    response_object = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt))

    if response_object.usage_metadata is None:
        raise Exception("Usage metrics returned None!")

    #Print token usage to the screen
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response_object.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response_object.usage_metadata.candidates_token_count}")

    # model is aware of messages and tool requests made
    for candidate in response_object.candidates:
        messages.append(candidate.content)

    results=[]
    
    if response_object.function_calls is None:
        print(response_object.text)
        print('Empty response object exiting status 0')
        exit(0)

    else:
        for function_call in response_object.function_calls:

            # passing the function calls from the AI model to my functions!
            function_call_result = call_function(function_call,args.verbose)

            if function_call_result.parts == []:
                raise Exception ("Empty function call result")
            
            if function_call_result.parts[0].function_response is None:
                raise Exception ("Function response is None")
            
            if function_call_result.parts[0].function_response.response is None:
                raise Exception ("Function response response is None")
            
            results.append(function_call_result.parts[0].function_response.response)

            messages.append(types.Content(role="user", parts=function_call_result.parts))

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            
print (f'Maximum number of permitted iterations reached') 
exit(1)
