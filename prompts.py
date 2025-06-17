# Currently no additional prompts used beyond the fallback in fallback_llm.py
# You can define reusable prompts or templates here if needed in the future.

fallback_prompt_template = """
You are a sales assistant. Given the sentence: \"{text}\", extract an objection and suggest a response.

If no objection, say: Objection: None\nSuggestion: Drop your email and contact number for follow-up. None.
Output format:
Objection: <...>
Suggestion: <...>
"""
