import time
from google.genai import errors


def generate_with_retry(client, model, prompt, retries=3):

    for attempt in range(retries):

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            return response.text or ""

        except errors.ServerError:

            if attempt < retries - 1:

                wait_time = 2 ** attempt

                time.sleep(wait_time)

            else:
                return "Server overloaded. Please try again later."

        except Exception as e:

            return f"Error: {e}"