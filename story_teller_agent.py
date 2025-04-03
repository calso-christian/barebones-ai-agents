from typing import Optional
from pydantic import BaseModel, Field
from openai import OpenAI

import os
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
    title: str = Field(min_length=5, max_length=100, description="Title of the Story")
    setting: str = Field(min_length=10, max_length=500, description="When and where the story will take place")
    main_character: str = Field(min_length=2, max_length=50, description="The protagonist of the Story")
    conflict: str = Field(min_length=10, max_length=500, description="The challenge or the problem of the story")

class StoryChapters(BaseModel):

    chapters: Dict[str, str] = Field(description="A dictionary of chapter summaries")

    # chapter_1: str = Field(description="First Chapter of the story")
    # chapter_2: str = Field(description="Second Chapter of the story")
    # chapter_3: str = Field(description="Third Chapter Chapter of the story, includes climax")
    # chapter_4: str = Field(description="Last Chapter of the story, includes ending of the story")

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
                "content": "You're an expert story-teller. Extract the Genre and Theme described from the text"
            },
            {
                "role":"user",
                "content":user_input
            }
        ],
        response_format=StoryInput,
    )

    result = completion.choices[0].message.parsed

    logger.info(f"Extraction Complete - Genre: {result.genre}")
    logger.info(f"Extraction Complete - Theme: {result.theme}")

    return result

