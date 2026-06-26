from unittest import mock
from unittest.mock import Mock

from rest_framework.test import APITestCase


class TestSynthesizeSpeech(APITestCase):
    fixtures = []

    # ------------------------------------------------------------------ #
    # Success cases                                                        #
    # ------------------------------------------------------------------ #

    @mock.patch("apps.voice.services.synthesize_speech._call_tts")
    def test_synthesize_speech_case_1(self, mock_call_tts: Mock):
        """
        Case: Valid text is submitted for speech synthesis
        Expected: 200, audio_path returned in response
        """
        mock_call_tts.return_value = "media/voice_responses/abc123.mp3"

        response = self.client.post(
            "/api/v1/voice/synthesize-speech/",
            {"text": "Hello, I am your voice assistant."},
            format="json",
        )

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(
            response.data["audio_path"],
            "media/voice_responses/abc123.mp3",
        )
        mock_call_tts.assert_called_once_with("Hello, I am your voice assistant.")

    @mock.patch("apps.voice.services.synthesize_speech._call_tts")
    def test_synthesize_speech_case_2(self, mock_call_tts: Mock):
        """
        Case: Long text within allowed max_length is submitted
        Expected: 200, audio_path returned
        """
        long_text = "This is a longer sentence. " * 30  # ~810 chars, within 2000 limit
        mock_call_tts.return_value = "media/voice_responses/xyz789.mp3"

        response = self.client.post(
            "/api/v1/voice/synthesize-speech/",
            {"text": long_text},
            format="json",
        )

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(
            response.data["audio_path"],
            "media/voice_responses/xyz789.mp3",
        )

    # ------------------------------------------------------------------ #
    # Failure cases                                                        #
    # ------------------------------------------------------------------ #

    def test_synthesize_speech_case_3(self):
        """
        Case: text field is missing from request body
        Expected: 400 bad request
        """
        response = self.client.post(
            "/api/v1/voice/synthesize-speech/",
            {},
            format="json",
        )

        self.assertEqual(response.status_code, 400, response.data)

    def test_synthesize_speech_case_4(self):
        """
        Case: text is an empty string
        Expected: 400 bad request — DRF CharField rejects blank before service runs
        """
        response = self.client.post(
            "/api/v1/voice/synthesize-speech/",
            {"text": ""},
            format="json",
        )

        self.assertEqual(response.status_code, 400, response.data)

    def test_synthesize_speech_case_5(self):
        """
        Case: text exceeds max_length of 2000 characters
        Expected: 400 bad request (caught by serializer field validation)
        """
        response = self.client.post(
            "/api/v1/voice/synthesize-speech/",
            {"text": "x" * 2001},
            format="json",
        )

        self.assertEqual(response.status_code, 400, response.data)

    @mock.patch("apps.voice.services.synthesize_speech._call_tts")
    def test_synthesize_speech_case_6(self, mock_call_tts: Mock):
        """
        Case: OpenAI TTS API is unavailable (external call fails)
        Expected: 502, speech_synthesis_failed error code
        """
        from apps.core.exceptions import SpeechSynthesisFailedError
        mock_call_tts.side_effect = SpeechSynthesisFailedError("TTS API unavailable")

        response = self.client.post(
            "/api/v1/voice/synthesize-speech/",
            {"text": "Hello world"},
            format="json",
        )

        self.assertEqual(response.status_code, 502, response.data)
