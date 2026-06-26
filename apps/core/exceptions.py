from rest_framework.exceptions import APIException, NotFound
from rest_framework import status


class TranscriptionFailedError(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = "Audio transcription failed."
    default_code = "transcription_failed"


class ResponseGenerationFailedError(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = "AI response generation failed."
    default_code = "response_generation_failed"


class SpeechSynthesisFailedError(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = "Speech synthesis failed."
    default_code = "speech_synthesis_failed"


class VoiceSessionNotFoundError(NotFound):
    default_detail = "Voice session not found."
    default_code = "voice_session_not_found"
