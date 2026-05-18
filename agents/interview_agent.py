import time
from google.genai import errors
from utils.prompts import INTERVIEW_PROMPT
from utils.gemini_helper import generate_with_retry

def generate_interview_questions(client, resume, role):

    prompt = f"""
    {INTERVIEW_PROMPT}

    Target Role:
    {role}

    Resume:
    {resume}
    """

    retries = 5

    for attempt in range(retries):

        try:

            return generate_with_retry(
                client,
                "gemini-2.5-flash-lite",
                prompt
            )

        except errors.ServerError as e:

            if attempt < retries - 1:

                wait_time = 2 ** attempt

                print(f"503 Error. Retrying in {wait_time} seconds...")

                time.sleep(wait_time)

            else:
                return f"Interview generation failed after retries: {e}"