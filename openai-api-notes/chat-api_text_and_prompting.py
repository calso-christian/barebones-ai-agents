# Load environment variables
# ----------------------------------------------------------------------------------------
from dotenv import load_dotenv
load_dotenv()


# Import necessary Dependencies
# ----------------------------------------------------------------------------------------
import requests
from openai import OpenAI
from pydantic import BaseModel

# Create an instance of OpenAI client
# ----------------------------------------------------------------------------------------
client = OpenAI()


# Simple Text Genaration and Prompting using Chat Completions API
# ----------------------------------------------------------------------------------------
completion = client.chat.completions.create(
    model='gpt-4o',
    messages=[
        {
            "role": "user",
            "content": "Write a short song about a cow getting abducted by an alien"
        }
    ]
)

print(completion.choices[0].message.content)

# Prompting while using Roles; Developer, User, System
# ----------------------------------------------------------------------------------------
completion1 = client.chat.completions.create(
    model='gpt-4o',
    messages=[
        {
            "role": "developer",
            "content": "Explain like I'm a 5 year old"
        },
        {
            "role": "user",
            "content": "What is an AI Agent?"
        }
    ]
)

print(completion1.choices[0].message.content)

