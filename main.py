import argparse
import os 

from dotenv import load_dotenv
from google import genai 
from google.genai import types



def main():
    # Create a parser object 
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    # Define the arguments we want to accept
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    # parse the args the user provided 
    args = parser.parse_args() 

    load_dotenv()   
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    generate_content(client, messages)
    


def generate_content(client, messages):
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
    )

    # program will terminate when RunTimeError is raised
    if response is None or response.usage_metadata is None:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)
   

if __name__ == "__main__":
    main()
