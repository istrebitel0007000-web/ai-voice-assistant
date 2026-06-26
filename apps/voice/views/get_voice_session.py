from rest_framework import serializers as drf_serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.core.serializer import Serializer
from apps.voice.services import get_voice_session


class GetVoiceSessionResponseSerializer(Serializer):
    session_id = drf_serializers.IntegerField()
    transcribed_text = drf_serializers.CharField()
    ai_response_text = drf_serializers.CharField()
    response_audio_path = drf_serializers.CharField()
    status = drf_serializers.CharField()
    created_at = drf_serializers.DateTimeField()


class GetVoiceSessionView(APIView):
    """
    GET /api/v1/voice/sessions/{session_id}/detail/
    Returns the full detail of a single VoiceSession by ID.
    """

    def get(self, request, session_id: int):
        session = get_voice_session(session_id)

        response_serializer = GetVoiceSessionResponseSerializer({
            "session_id": session.id,
            "transcribed_text": session.transcribed_text,
            "ai_response_text": session.ai_response_text,
            "response_audio_path": session.response_audio_path,
            "status": session.status,
            "created_at": session.created_at,
        })
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)
