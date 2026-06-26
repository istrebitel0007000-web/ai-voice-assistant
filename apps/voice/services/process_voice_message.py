from apps.voice.models import VoiceSession
from apps.voice.services.transcribe_audio import transcribe_audio
from apps.voice.services.generate_response import generate_response
from apps.voice.services.synthesize_speech import synthesize_speech
from apps.core.exceptions import (
    TranscriptionFailedError,
    ResponseGenerationFailedError,
    SpeechSynthesisFailedError,
)


def process_voice_message(audio_file) -> VoiceSession:
    """
    Full voice pipeline: audio in → speech out.
    1. Transcribe audio to text (Whisper)
    2. Generate AI reply text (ChatGPT)
    3. Synthesize reply to audio (TTS)
    4. Save the full session to DB and return it.

    If any step fails its own exception is raised and the session
    is saved with status=FAILED so the failure is traceable.
    """
    session = _create_pending_session(audio_file)

    try:
        transcribed_text = transcribe_audio(audio_file)
        session = _save_transcription(session, transcribed_text)

        ai_response_text = generate_response(transcribed_text)
        session = _save_ai_response(session, ai_response_text)

        response_audio_path = synthesize_speech(ai_response_text)
        session = _save_completed(session, response_audio_path)

    except (
        TranscriptionFailedError,
        ResponseGenerationFailedError,
        SpeechSynthesisFailedError,
    ) as exc:
        _save_failed(session)
        raise exc

    return session


def _create_pending_session(audio_file) -> VoiceSession:
    return VoiceSession.objects.create(
        user_audio_path=getattr(audio_file, "name", "unknown"),
        status=VoiceSession.Status.PENDING,
    )


def _save_transcription(session: VoiceSession, transcribed_text: str) -> VoiceSession:
    session.transcribed_text = transcribed_text
    session.save(update_fields=["transcribed_text", "updated_at"])
    return session


def _save_ai_response(session: VoiceSession, ai_response_text: str) -> VoiceSession:
    session.ai_response_text = ai_response_text
    session.save(update_fields=["ai_response_text", "updated_at"])
    return session


def _save_completed(session: VoiceSession, response_audio_path: str) -> VoiceSession:
    session.response_audio_path = response_audio_path
    session.status = VoiceSession.Status.COMPLETED
    session.save(update_fields=["response_audio_path", "status", "updated_at"])
    return session


def _save_failed(session: VoiceSession) -> None:
    session.status = VoiceSession.Status.FAILED
    session.save(update_fields=["status", "updated_at"])
