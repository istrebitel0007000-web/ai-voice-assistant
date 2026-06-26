from unittest import mock
from unittest.mock import Mock

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase


class TestTranscribeAudio(APITestCase):
    fixtures = []  # No DB fixtures needed — no auth required for this endpoint in tests

    # ------------------------------------------------------------------ #
    # Success cases                                                        #
    # ------------------------------------------------------------------ #

    @mock.patch("apps.voice.services.transcribe_audio._call_whisper")
    def test_transcribe_audio_case_1(self, mock_call_whisper: Mock):
        """
        Case: Valid WAV audio file is submitted
        Expected: 200, transcribed_text returned in response
        """
        mock_call_whisper.return_value = "Hello, how are you?"

        audio_file = SimpleUploadedFile(
            name="test.wav",
            content=b"fake-audio-bytes",
            content_type="audio/wav",
        )
        response = self.client.post(
            "/api/v1/voice/transcribe/",
            {"audio": audio_file},
            format="multipart",
        )

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["transcribed_text"], "Hello, how are you?")
        mock_call_whisper.assert_called_once()

    @mock.patch("apps.voice.services.transcribe_audio._call_whisper")
    def test_transcribe_audio_case_2(self, mock_call_whisper: Mock):
        """
        Case: Valid MP3 audio file is submitted
        Expected: 200, transcribed_text returned in response
        """
        mock_call_whisper.return_value = "What is the weather today?"

        audio_file = SimpleUploadedFile(
            name="test.mp3",
            content=b"fake-audio-bytes",
            content_type="audio/mpeg",
        )
        response = self.client.post(
            "/api/v1/voice/transcribe/",
            {"audio": audio_file},
            format="multipart",
        )

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["transcribed_text"], "What is the weather today?")

    # ------------------------------------------------------------------ #
    # Failure cases                                                        #
    # ------------------------------------------------------------------ #

    def test_transcribe_audio_case_3(self):
        """
        Case: No audio file provided in request
        Expected: 400 bad request
        """
        response = self.client.post(
            "/api/v1/voice/transcribe/",
            {},
            format="multipart",
        )

        self.assertEqual(response.status_code, 400, response.data)

    def test_transcribe_audio_case_4(self):
        """
        Case: Unsupported file type (text/plain) submitted
        Expected: 502, transcription_failed error code
        """
        bad_file = SimpleUploadedFile(
            name="test.txt",
            content=b"this is not audio",
            content_type="text/plain",
        )
        response = self.client.post(
            "/api/v1/voice/transcribe/",
            {"audio": bad_file},
            format="multipart",
        )

        self.assertEqual(response.status_code, 502, response.data)

    @mock.patch("apps.voice.services.transcribe_audio._call_whisper")
    def test_transcribe_audio_case_5(self, mock_call_whisper: Mock):
        """
        Case: OpenAI Whisper API is unavailable (external call fails)
        Expected: 502, transcription_failed error code
        """
        from apps.core.exceptions import TranscriptionFailedError
        mock_call_whisper.side_effect = TranscriptionFailedError("API unavailable")

        audio_file = SimpleUploadedFile(
            name="test.wav",
            content=b"fake-audio-bytes",
            content_type="audio/wav",
        )
        response = self.client.post(
            "/api/v1/voice/transcribe/",
            {"audio": audio_file},
            format="multipart",
        )

        self.assertEqual(response.status_code, 502, response.data)
