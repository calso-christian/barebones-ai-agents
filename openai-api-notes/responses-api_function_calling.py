# Load environment variables
# ----------------------------------------------------------------------------------------
from dotenv import load_dotenv
import os
load_dotenv()



# Import necessary Dependencies
# ----------------------------------------------------------------------------------------
import json
from openai import OpenAI
import requests
from pydantic import BaseModel, Field

# Create an instance of OpenAI client
# ----------------------------------------------------------------------------------------
client = OpenAI()

tools =[
    {
        "type" : "function",
        "name" : "get_weather",
        "description" : "Get current Temperature for provided coordinates in celsius",
        "parameters" : {
            "type" : "object",
            "properties" : {
                "latitude" : {"type" : "number"},
                "longitude" : {"type" : "number"},
            },
            "required" : ["latitude", "longitude"],
            "additionalProperties" : False
        },
        "strict" : True
    }
]   


def get_weather(latitude, longitude):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']

system_prompt="You're a helpful weather assistant"
user_prompt="What's the weather like in Ibaraki, Japan?"


input_message=[
    {"role":"system", "content":system_prompt},
    {"role":"user", "content":user_prompt}
]

response=client.responses.create(
    model='gpt-4o',
    input=input_message,
    tools=tools,
)


print(json.dumps(response.model_dump(), indent=4))


def call_function(name, args):
    if name == 'get_weather':
        return get_weather(**args)
    else:
        return {"error": "Unknown function call"}


if hasattr(response, "output") and response.output:
    tool_calls=response.output

    for tool_call in tool_calls:
        name=tool_call.name
        args=json.loads(tool_call.arguments)
        #input_message.append(response.output)

        result=call_function(name,args)
        input_message.append(tool_call)

        input_message.append({
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": json.dumps(result)  # Convert result to string
        })



    response_2 = client.responses.create(
        model="gpt-4o",
        input=input_message,
        tools=tools,
    )

    output = response_2.output_text

    print(output)
else:
    print("No tool calls were requested")