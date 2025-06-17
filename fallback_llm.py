import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_fallback_objection(text: str):
    prompt = f"""
You are a sales assistant. Given the sentence: \"{text}\", extract an objection and suggest a response.

If no objection, say: Objection: None\nSuggestion: Drop your email and contact number for follow-up. None.
Output format:
Objection: <...>
Suggestion: <...>
"""

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.3
    )
    content = response.choices[0].message.content.strip()

    if "Objection: None" in content:
        return None, None

    try:
        obj = content.split("Objection:")[1].split("Suggestion:")[0].strip()
        sug = content.split("Suggestion:")[1].strip()
        return obj, sug
    except Exception:
        return "Unknown", content
