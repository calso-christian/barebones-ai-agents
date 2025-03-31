# Load environment variables
# ----------------------------------------------------------------------------------------
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
load_dotenv()



# Import necessary Dependencies
# ----------------------------------------------------------------------------------------
import json
from openai import OpenAI

# Create an instance of OpenAI client
# ----------------------------------------------------------------------------------------
client = OpenAI()


# Create a function that sends out Email - The tool will call this function
# ----------------------------------------------------------------------------------------
def email_sending(to_email,subject,body):
    EMAIL_ADDRESS = "christianpaulcalso@gmail.com"
    EMAIL_PASSWORD = os.getenv("GOOGLE_APP_PW")

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())

        print(f"✅ Email sent successfully to {to_email}!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# Create a tool -- Define the structured output for the Email
# ----------------------------------------------------------------------------------------
tools = [
    {
        "type" : "function",
        "function" : {
            "name" : "send_email",
            "description" : "Send an Email to a given recipient with a given subject and message",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "to" : {
                        "type" : "string",
                        "description" : "The recipient Email"
                    },
                    "subject": {
                        "type" : "string",
                        "description":"Email subject line"
                    },
                    "body": {
                        "type" : "string",
                        "description" : "Body of the Email"
                    },
                },
                "required" : ["to","subject","body"],
                "additionalProperties" : False
            },
            "strict" : True
        }
    }
]

completion = client.chat.completions.create(
    model='gpt-4o',
    messages=[{"role":"user",
               "content" : "Can you send an Email to therealclaire25@gmail.com saying how much I love her, Make the subject cheesy make it at least 2 paragraphs long and for regards put your future husband Christian Calso"
               }],
    tools=tools)

#print(completion.choices[0].message.tool_calls)



if completion.choices[0].message.tool_calls:
    tool_call = completion.choices[0].message.tool_calls[0]

    # Check if the function name is "send_email"
    if tool_call.function.name == "send_email":
        args = json.loads(tool_call.function.arguments)  # Extract arguments
        print("📧 Sending email with the following details:")
        print(args)  # Debugging: Show the extracted arguments

        # Call the function with extracted arguments
        email_sending(args["to"], args["subject"], args["body"])