import os
import json
from dotenv import load_dotenv
from groq import Groq


load_dotenv(verbose=True)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def classify_and_extract_news(news_content):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"{json.dumps(news_content)}\n\n"
                        "This is an article. I want to analyze a few things:\n"
                        "1. In what country did it happen?\n"
                        "2. Classify the article into one of the following categories: General news, Historical terror attack, or Current terror attack.\n\n"
                        "if you don't find something please put in the field None"
                        "After analyzing, provide a JSON with the following structure:\n"
                        "{\n"
                        "   \"category\": \"str\",\n"
                        "   \"country\": \"str\",\n"
                        "   \"city\": \"str\",\n"
                        "   \"region\": \"str\",\n"
                        "}\n\n"
                        "Respond with the JSON only, without any extra text."
                    ),
                }
            ],
            model="llama3-8b-8192",
        )

        response = chat_completion.choices[0].message.content
        try:
            parsed_response = json.loads(response)
            return parsed_response
        except json.JSONDecodeError as e:
            return f"Error parsing response: {str(e)}"

    except Exception as e:
        return f"Error during API call: {str(e)}"

