import openai

from apps.core.exceptions import TranscriptionFailedError


def transcribe_audio(audio_file) -> str:
    """
    Transcribe audio to text using OpenAI Whisper.
    Returns the transcribed text string.
    Raises TranscriptionFailedError if the external call fails.
    """
    _validate_audio_file(audio_file)
    return _call_whisper(audio_file)


def _validate_audio_file(audio_file) -> None:
    if audio_file is None:
        raise TranscriptionFailedError("No audio file provided.")

    allowed_types = {"audio/mpeg", "audio/wav", "audio/webm", "audio/mp4", "audio/ogg"}
    content_type = getattr(audio_file, "content_type", "")
    if content_type not in allowed_types:
        raise TranscriptionFailedError(
            f"Unsupported audio type '{content_type}'. "
            f"Allowed: {', '.join(allowed_types)}"
        )


def _call_whisper(audio_file) -> str:
    try:
        client = openai.OpenAI()
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text",
        )
        return transcript.strip()
    except openai.OpenAIError as exc:
        raise TranscriptionFailedError(str(exc)) from exc
