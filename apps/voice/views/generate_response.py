from rest_framework import serializers as drf_serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.core.serializer import Serializer
from apps.voice.services import generate_response


class GenerateResponseRequestSerializer(Serializer):
    user_text = drf_serializers.CharField(required=True, max_length=2000)


class GenerateResponseResponseSerializer(Serializer):
    ai_response_text = drf_serializers.CharField()


class GenerateResponseView(APIView):
    """
    POST /api/v1/voice/generate-response/
    Accepts transcribed user text, returns AI-generated reply text.
    """

    def post(self, request):
        request_serializer = GenerateResponseRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        ai_response_text = generate_response(
            request_serializer.validated_data["user_text"]
        )

        response_serializer = GenerateResponseResponseSerializer(
            {"ai_response_text": ai_response_text}
        )
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)
