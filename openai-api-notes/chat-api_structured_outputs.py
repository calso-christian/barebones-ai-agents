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

# Create class definition for Structured Output Format
# ----------------------------------------------------------------------------------------
class Step(BaseModel):
    explanation: str

class Recipe(BaseModel):
    ingredient: str

class ChefNotes(BaseModel):
    steps: list[Step]
    recipe: list[Recipe]

# Create an instance of Chat Completion API
# ----------------------------------------------------------------------------------------
completion = client.beta.chat.completions.parse(
    model='gpt-4o',
    messages=[
        {"role": "system", "content":"You are a worldwide known helpful chef. Guide the user through your cooking steps"},
        {"role": "user", "content": "Help me cook binangkal"}
    ],
# Pass the output into the ChefNotes for formatting
# ----------------------------------------------------------------------------------------
    response_format=ChefNotes,
)

chef_steps = completion.choices[0].message

if (chef_steps.refusal):
    print(chef_steps.refusal)
else:
    print(chef_steps.parsed)