from apps.voice.models import VoiceSession


def delete_all_voice_sessions() -> int:
    """
    Delete all VoiceSessions from the database.
    Returns the count of deleted sessions.
    """
    return _delete_all()


def _delete_all() -> int:
    count, _ = VoiceSession.objects.all().delete()
    return count
