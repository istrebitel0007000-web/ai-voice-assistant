from apps.voice.models import VoiceSession
from apps.core.exceptions import VoiceSessionNotFoundError


def get_voice_session(session_id: int) -> VoiceSession:
    """
    Fetch a single VoiceSession by its ID.
    Raises VoiceSessionNotFoundError if the session does not exist.
    """
    return _fetch_session(session_id)


def _fetch_session(session_id: int) -> VoiceSession:
    try:
        return VoiceSession.objects.get(id=session_id)
    except VoiceSession.DoesNotExist:
        raise VoiceSessionNotFoundError()
