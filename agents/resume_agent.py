from google import genai
from utils.prompts import RESUME_PROMPT
from utils.gemini_helper import generate_with_retry

def analyze_resume(client, resume, role):

    prompt = f"""
    Current Year: 2026
    {RESUME_PROMPT}

    Target Role:
    {role}

    Resume:
    {resume}
    """

    return generate_with_retry(
        client,
        "gemini-2.5-flash-lite",
        prompt
    )