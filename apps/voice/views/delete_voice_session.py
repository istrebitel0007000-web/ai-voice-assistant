from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.voice.services import delete_voice_session


class DeleteVoiceSessionView(APIView):
    """
    DELETE /api/v1/voice/sessions/{session_id}/delete/
    Permanently deletes a single VoiceSession by ID.
    Returns 204 No Content on success.
    """

    def delete(self, request, session_id: int):
        delete_voice_session(session_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
