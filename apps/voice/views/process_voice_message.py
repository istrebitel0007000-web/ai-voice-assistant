from rest_framework import serializers as drf_serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from apps.core.serializer import Serializer
from apps.voice.services import process_voice_message


class ProcessVoiceMessageRequestSerializer(Serializer):
    audio = drf_serializers.FileField(required=True)


class ProcessVoiceMessageResponseSerializer(Serializer):
    session_id = drf_serializers.IntegerField()
    transcribed_text = drf_serializers.CharField()
    ai_response_text = drf_serializers.CharField()
    response_audio_path = drf_serializers.CharField()
    status = drf_serializers.CharField()


class ProcessVoiceMessageView(APIView):
    """
    POST /api/v1/voice/process/
    Full pipeline: upload audio → get back AI voice response.
    Runs transcription → AI reply → speech synthesis in one request.
    """
    parser_classes = [MultiPartParser]

    def post(self, request):
        request_serializer = ProcessVoiceMessageRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        session = process_voice_message(
            request_serializer.validated_data["audio"]
        )

        response_serializer = ProcessVoiceMessageResponseSerializer({
            "session_id": session.id,
            "transcribed_text": session.transcribed_text,
            "ai_response_text": session.ai_response_text,
            "response_audio_path": session.response_audio_path,
            "status": session.status,
        })
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)
