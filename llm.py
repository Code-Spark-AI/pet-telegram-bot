from openai import OpenAI
from dotenv import load_dotenv
import os
from prompt import get_prompt;

# Load environment variables
load_dotenv()

client = OpenAI(
    # Defaults to os.environ.get("OPENAI_API_KEY")
)

openai_api_key = os.getenv("OPENAI_API_KEY")

def generate_cron_expression(text):
    prompt = get_prompt(text)
    response = client.chat.completions.create(
        prompt,
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello world"}]
)
    cron_expression = response.choices[0].text.strip()
    print(cron_expression)
    return cron_expression

