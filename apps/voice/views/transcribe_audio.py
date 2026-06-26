from rest_framework import serializers as drf_serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from apps.core.serializer import Serializer
from apps.voice.services import transcribe_audio


class TranscribeAudioRequestSerializer(Serializer):
    audio = drf_serializers.FileField(required=True)


class TranscribeAudioResponseSerializer(Serializer):
    transcribed_text = drf_serializers.CharField()


class TranscribeAudioView(APIView):
    """
    POST /api/v1/voice/transcribe/
    Accepts a multipart audio file, returns its transcribed text.
    """
    parser_classes = [MultiPartParser]

    def post(self, request):
        request_serializer = TranscribeAudioRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        transcribed_text = transcribe_audio(
            request_serializer.validated_data["audio"]
        )

        response_serializer = TranscribeAudioResponseSerializer(
            {"transcribed_text": transcribed_text}
        )
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)
