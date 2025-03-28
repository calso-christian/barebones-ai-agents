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


# Simple Text Genaration and Prompting using Responses API
# ----------------------------------------------------------------------------------------
responses = client.responses.create(
    model='gpt-4o',
    input='What is the most used AI Agent Framework?'
)

print(responses.output_text)

# Using Instructions atribute when prompting in Responses API
# ----------------------------------------------------------------------------------------
responses1 = client.responses.create(
    model='gpt-4o',
    instructions='Don\'t use any jargons. Give reference as well',
    input='How to create a an AI Agent that sendout email'
)

print(responses1.output_text)


# Much like the Chat Completions API, the {role, content} syntax can also be used
# ----------------------------------------------------------------------------------------
responses2 = client.responses.create(
    model='gpt-4o',
    input=[
        {
            "role":'developer',
            "content": "You're a Helpful assistant Knowledgable about Programming languages, but you are stuttering"
        },
        {
            "role": "user",
            "content": "What is python pydantic?"
        }
    ]
)

print(responses2.output_text)