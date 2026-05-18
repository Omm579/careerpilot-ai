from google import genai
from utils.prompts import SKILL_GAP_PROMPT
from utils.gemini_helper import generate_with_retry

def analyze_skill_gap(client, resume, role):

    prompt = f"""
    {SKILL_GAP_PROMPT}

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