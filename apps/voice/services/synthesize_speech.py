import uuid
import os

import openai

from apps.core.exceptions import SpeechSynthesisFailedError

_AUDIO_OUTPUT_DIR = "media/voice_responses"


def synthesize_speech(text: str) -> str:
    """
    Convert text to speech using OpenAI TTS.
    Saves the audio file to disk and returns its relative file path.
    Raises SpeechSynthesisFailedError if the external call fails.
    """
    _validate_text(text)
    return _call_tts(text)


def _validate_text(text: str) -> None:
    if not text or not text.strip():
        raise SpeechSynthesisFailedError("Text must not be empty.")


def _build_output_path() -> str:
    os.makedirs(_AUDIO_OUTPUT_DIR, exist_ok=True)
    filename = f"{uuid.uuid4()}.mp3"
    return os.path.join(_AUDIO_OUTPUT_DIR, filename)


def _call_tts(text: str) -> str:
    try:
        client = openai.OpenAI()
        output_path = _build_output_path()
        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="alloy",
            input=text,
        ) as response:
            response.stream_to_file(output_path)
        return output_path
    except openai.OpenAIError as exc:
        raise SpeechSynthesisFailedError(str(exc)) from exc
