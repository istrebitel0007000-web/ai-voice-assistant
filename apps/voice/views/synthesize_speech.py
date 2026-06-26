from rest_framework import serializers as drf_serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.core.serializer import Serializer
from apps.voice.services import synthesize_speech


class SynthesizeSpeechRequestSerializer(Serializer):
    text = drf_serializers.CharField(required=True, max_length=2000)


class SynthesizeSpeechResponseSerializer(Serializer):
    audio_path = drf_serializers.CharField()


class SynthesizeSpeechView(APIView):
    """
    POST /api/v1/voice/synthesize-speech/
    Accepts text, returns the path to the generated audio file.
    """

    def post(self, request):
        request_serializer = SynthesizeSpeechRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        audio_path = synthesize_speech(
            request_serializer.validated_data["text"]
        )

        response_serializer = SynthesizeSpeechResponseSerializer(
            {"audio_path": audio_path}
        )
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)
