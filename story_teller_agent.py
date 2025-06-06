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
    is_story_worthy: bool = Field()
    

class StoryOutline(BaseModel):
    title: str = Field(description="Title of the Story")
    setting: str = Field(description="When and where the story will take place")
    main_character: str = Field(description="The protagonist of the Story")
    conflict: str = Field(description="The challenge or the problem of the story")

class StoryChapters(BaseModel):

    chapters: Dict[str, str] = Field(..., description="A dictionary of chapter summaries")

class StoryChaptersParagraphs(BaseModel):
    chapters: Dict[str, List[str]] = Field(..., description="A dictionary of chapter summaries")

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

    logger.info(F"Extraction Complete")
    logger.info(f"Genre: {result.genre}")
    logger.info(f"Theme: {result.theme}")


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

    logger.info(f"Outline Created")
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


        logger.info(f"Chapter Summaries Generated")
        for chapter, summary in validated.chapters.items():
            logger.info(f"{chapter}: {summary}")
        


        return validated

    except ValidationError as ve:
        logger.error(f"Pydantic validation failed: {ve}")
        raise

    except Exception as e:
        logger.error(f"Failed to generate chapter summaries: {e}")
        raise


def paragraphs_per_chapter(chapters) -> StoryChaptersParagraphs:
    logger.info("Analyzing chapters, creating paragraphs of the story")

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role":"system",
                    "content":"You're a professional story architect. Based on the given chapter summaries, "
                    "generate paragraphs to complete each chapters to build the whole story.\n"
                    "Your response should be a JSON object that follows this structure:\n"
                    "{\n"
                    "  \"chapters\": {\n"
                    "    \"chapter_1\": [\"Paragraph 1...\", \"Paragraph 2...\"],\n"
                    "    \"chapter_2\": [\"Paragraph 1...\", \"Paragraph 2...\"]\n"
                    "  }\n"
                    "}\n"
                    "Each chapter should contain a list of paragraphs that expand on the summary.\n"
                    "Only return the JSON object in the specified format, without any extra explanation."
                },
                {
                    "role":"user",
                    "content":json.dumps(chapters.dict())
                }
            ],
            response_format={"type": "json_object"} 
        )

        raw_content = completion.choices[0].message.content
        logger.debug(f"Raw response: {raw_content}")

        parsed_json = json.loads(raw_content)
        validated = StoryChaptersParagraphs(**parsed_json)

        logger.info(f"Story Completed")
        # for chapter, paragraphs in validated.chapters.items():
        #     logger.info(f"Chapter: {chapter}")
        #     for idx, paragraph in enumerate(paragraphs, 1):
        #         logger.info(f"  Paragraph {idx}: {paragraph}")

        return validated

    except ValidationError as ve:
        logger.error(f"Pydantic validation failed: {ve}")
        raise

    except Exception as e:
        logger.error(f"Failed to generate chapter summaries: {e}")
        raise



def agent_execution(user_input: str):
    
    
    pass

inputs=story_details_extraction("A man wakes up to find his reflection "
"missing from every mirror—until he hears it whisper from behind him, 'Don't turn around.'"
)

outline=create_story_outline(inputs)

chapters=create_chapter_summaries(outline)

paragraphs_per_chapter(chapters)