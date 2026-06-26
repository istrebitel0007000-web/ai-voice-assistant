from apps.voice.models import VoiceSession
from apps.core.exceptions import VoiceSessionNotFoundError


def delete_voice_session(session_id: int) -> None:
    """
    Delete a single VoiceSession by its ID.
    Raises VoiceSessionNotFoundError if the session does not exist.
    """
    session = _fetch_session(session_id)
    _delete(session)


def _fetch_session(session_id: int) -> VoiceSession:
    try:
        return VoiceSession.objects.get(id=session_id)
    except VoiceSession.DoesNotExist:
        raise VoiceSessionNotFoundError()


def _delete(session: VoiceSession) -> None:
    session.delete()
