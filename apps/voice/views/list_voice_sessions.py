from rest_framework import serializers as drf_serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.core.serializer import Serializer
from apps.voice.services import list_voice_sessions


class ListVoiceSessionsItemSerializer(Serializer):
    session_id = drf_serializers.IntegerField()
    transcribed_text = drf_serializers.CharField()
    ai_response_text = drf_serializers.CharField()
    response_audio_path = drf_serializers.CharField()
    status = drf_serializers.CharField()
    created_at = drf_serializers.DateTimeField()


class ListVoiceSessionsView(APIView):
    """
    GET /api/v1/voice/sessions/list/
    Returns all VoiceSessions ordered by most recent first.
    """

    def get(self, request):
        sessions = list_voice_sessions()

        response_serializer = ListVoiceSessionsItemSerializer(sessions, many=True)
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)
