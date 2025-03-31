# Load environment variables
# ----------------------------------------------------------------------------------------
from dotenv import load_dotenv
load_dotenv()


# Import necessary Dependencies
# ----------------------------------------------------------------------------------------
import requests
import json
from openai import OpenAI


client = OpenAI()

response = client.responses.create(
    model='gpt-4o',
    input=[
        {"role":"system","content":"You're a useful assistant, extract details from the text"},
        {"role":"user","content":"""To cook a delicious adobo, start by gathering the ingredients: 1 kg of chicken or pork (or a mix of both), 1 cup of soy sauce, ½ cup of vinegar, 1 cup of water, 6 cloves of garlic (minced), 1 onion (sliced), 2 bay leaves, 1 teaspoon of whole peppercorns, and 1 tablespoon of sugar. You can also add potatoes or boiled eggs for extra texture.
        Begin by heating a pan over medium heat and adding a little oil. Sauté the garlic and onion until fragrant. Then, add the meat and cook until it turns slightly brown. Pour in the soy sauce, followed by the vinegar, without stirring, and let it simmer for a few minutes. Add the bay leaves, peppercorns, and water, then cover the pan and let it simmer for about 30–40 minutes or until the meat is tender. Stir occasionally and adjust the seasoning by adding sugar to balance the flavors. If you prefer a thicker sauce, let it simmer uncovered for a few more minutes until the sauce reduces. Once done, serve your adobo hot with steamed rice. Enjoy!"""}
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "cooking_steps",
            "schema": {
                "type": "object",
                "properties": {
                    "ingredients": {
                        "type": "array",
                        "items":{
                            "type": "object",
                            "properties":{
                                "ingredient":{"type":"string"}
                            },
                            "required":["ingredient"],
                            "additionalProperties": False
                        }
                    },
                    "steps": {
                        "type": "array",
                        "items":{
                            "type": "object",
                            "properties":{
                                "step":{"type":"string"}
                            },
                            "required":["step"],
                            "additionalProperties": False
                        }
                    },
                },
                "required": ["ingredients", "steps"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
)

cook = json.loads(response.output_text)
print(cook)