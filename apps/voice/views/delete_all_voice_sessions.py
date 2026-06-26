from rest_framework import serializers as drf_serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.core.serializer import Serializer
from apps.voice.services import delete_all_voice_sessions


class DeleteAllVoiceSessionsResponseSerializer(Serializer):
    deleted_count = drf_serializers.IntegerField()


class DeleteAllVoiceSessionsView(APIView):
    """
    DELETE /api/v1/voice/sessions/delete-all/
    Permanently deletes all VoiceSessions.
    Returns 200 with count of deleted sessions.
    """

    def delete(self, request):
        deleted_count = delete_all_voice_sessions()

        response_serializer = DeleteAllVoiceSessionsResponseSerializer(
            {"deleted_count": deleted_count}
        )
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)
