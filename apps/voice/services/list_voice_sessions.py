from typing import List, Dict

from apps.voice.models import VoiceSession


def list_voice_sessions() -> List[Dict]:
    """
    Return all VoiceSessions as a list of dicts, ordered by most recent first.
    Shaping data here keeps the view clean with no iteration logic.
    """
    sessions = _fetch_all_sessions()
    return _serialize_sessions(sessions)


def _fetch_all_sessions():
    return VoiceSession.objects.all()


def _serialize_sessions(sessions) -> List[Dict]:
    return [
        {
            "session_id": s.id,
            "transcribed_text": s.transcribed_text,
            "ai_response_text": s.ai_response_text,
            "response_audio_path": s.response_audio_path,
            "status": s.status,
            "created_at": s.created_at,
        }
        for s in sessions
    ]
