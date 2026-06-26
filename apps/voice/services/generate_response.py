import openai

from apps.core.exceptions import ResponseGenerationFailedError

_SYSTEM_PROMPT = (
    "You are a helpful, friendly voice assistant. "
    "Give clear and concise answers suitable for spoken responses. "
    "Keep replies under 100 words unless more detail is truly necessary."
)


def generate_response(user_text: str) -> str:
    """
    Generate an AI text response for the given user message.
    Returns the assistant reply as a plain string.
    Raises ResponseGenerationFailedError if the external call fails.
    """
    _validate_user_text(user_text)
    return _call_chat(user_text)


def _validate_user_text(user_text: str) -> None:
    if not user_text or not user_text.strip():
        raise ResponseGenerationFailedError("User text must not be empty.")


def _call_chat(user_text: str) -> str:
    try:
        client = openai.OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            max_tokens=200,
            temperature=0.7,
        )
        return completion.choices[0].message.content.strip()
    except openai.OpenAIError as exc:
        raise ResponseGenerationFailedError(str(exc)) from exc
