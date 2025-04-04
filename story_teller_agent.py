from typing import Optional
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI

import os, json
import logging
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()


# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


client=OpenAI()
model='gpt-4o'

class StoryInput(BaseModel):
    # User Input Validation

    genre: str = Field(description="The genre of the story (e.g., Fantasy, Scifi, Drama)")
    theme: str = Field(description="The idea of the whole story")
    

class StoryOutline(BaseModel):
    title: str = Field(description="Title of the Story")
    setting: str = Field(description="When and where the story will take place")
    main_character: str = Field(description="The protagonist of the Story")
    conflict: str = Field(description="The challenge or the problem of the story")

class StoryChapters(BaseModel):

    chapters: Dict[str, str] = Field(..., description="A dictionary of chapter summaries")

class StoryChaptersParagraphs(BaseModel):
    paragraphs: List[str] = Field(description="List of detailed paragraphs for each chapter")

    # openingParagraph: str = Field(description="Includes all chapter 1 of the story")
    # buildUpParagraph: str = Field(description="Includes chapter 2 and all the build of the story")
    # climaxParagraph: str = Field(description="Includes chapter 3, and climax of the story")
    # endingParagraph: str = Field(description="Includes ending of the story")

def story_details_extraction(user_input: str) -> StoryInput:
    
    logger.info("Starting story details extraction and analysis")
    logger.debug(f"Input Text: {user_input}")

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role":"system",
                "content": "You're an expert story-teller."
                " Extract the Genre and Theme described from the text"
            },
            {
                "role":"user",
                "content":user_input
            }
        ],
        response_format=StoryInput,
    )

    result = completion.choices[0].message.parsed

    #logger.info(F"Extraction Complete = Raw: {completion.choices[0].message}")
    logger.info(f"Extraction Complete - Genre: {result.genre}")
    logger.info(f"Extraction Complete - Theme: {result.theme}")

    return f"Story Details - {result.genre}: {result.theme}"


def create_story_outline(extracted_theme_genre: str) -> StoryOutline:
    input=extracted_theme_genre

    logger.info('Creating Story Outline ...')

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role":"system",
                "content": "You're an expert story-teller. "
                "Extract the necessary info from the Given Genre and Theme"
            },
            {
                "role":"user",
                "content":input
            }
        ],
        response_format=StoryOutline,
    )

    result = completion.choices[0].message.parsed

    logger.info(f"Story Title: {result.title}")
    logger.info(f"Story Setting: {result.setting}")
    logger.info(f"Story Main Character: {result.main_character}")
    logger.info(f"Story Conflict: {result.conflict}")

    return json.dumps(result.model_dump())


def create_chapter_summaries(story_outline: str) -> StoryChapters:
    logger.info("Creating chapter summaries from story outline...")

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You're a professional story architect. Based on the given story outline, "
                        "generate a set of chapter summaries. Return a JSON object like:\n"
                        "{\n"
                        "  \"chapters\": {\n"
                        "    \"chapter_1\": \"Summary...\",\n"
                        "    \"chapter_2\": \"Summary...\"\n"
                        "  }\n"
                        "}\n"
                        "Only return the JSON object, no extra explanation."
                    )
                },
                {
                    "role": "user",
                    "content": story_outline
                }
            ],
            response_format={"type": "json_object"} 
        )

        raw_content = completion.choices[0].message.content
        logger.debug(f"Raw response: {raw_content}")

        parsed_json = json.loads(raw_content)

        validated = StoryChapters(**parsed_json)

        for chapter, summary in validated.chapters.items():
            logger.info(f"{chapter}: {summary}")


        return validated

    except ValidationError as ve:
        logger.error(f"Pydantic validation failed: {ve}")
        raise

    except Exception as e:
        logger.error(f"Failed to generate chapter summaries: {e}")
        raise




inputs=story_details_extraction("A man wakes up to find his reflection "
"missing from every mirror—until he hears it whisper from behind him, 'Don't turn around.'"
)

outline=create_story_outline(inputs)

create_chapter_summaries(outline)