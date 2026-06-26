from unittest import mock
from unittest.mock import Mock

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from apps.voice.models import VoiceSession


class TestProcessVoiceMessage(APITestCase):
    fixtures = []

    def _make_audio_file(self):
        return SimpleUploadedFile(
            name="test.wav",
            content=b"fake-audio-bytes",
            content_type="audio/wav",
        )

    # ------------------------------------------------------------------ #
    # Success cases                                                        #
    # ------------------------------------------------------------------ #

    @mock.patch("apps.voice.services.transcribe_audio._call_whisper")
    @mock.patch("apps.voice.services.generate_response._call_chat")
    @mock.patch("apps.voice.services.synthesize_speech._call_tts")
    def test_process_voice_message_case_1(
        self,
        mock_call_tts: Mock,
        mock_call_chat: Mock,
        mock_call_whisper: Mock,
    ):
        """
        Case: Valid audio file submitted, all external services respond successfully
        Expected: 200, full response returned, VoiceSession saved as COMPLETED
        """
        mock_call_whisper.return_value = "What is the capital of France?"
        mock_call_chat.return_value = "The capital of France is Paris."
        mock_call_tts.return_value = "media/voice_responses/abc123.mp3"

        response = self.client.post(
            "/api/v1/voice/process/",
            {"audio": self._make_audio_file()},
            format="multipart",
        )

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["transcribed_text"], "What is the capital of France?")
        self.assertEqual(response.data["ai_response_text"], "The capital of France is Paris.")
        self.assertEqual(response.data["response_audio_path"], "media/voice_responses/abc123.mp3")
        self.assertEqual(response.data["status"], VoiceSession.Status.COMPLETED)

        session = VoiceSession.objects.get(id=response.data["session_id"])
        self.assertEqual(session.transcribed_text, "What is the capital of France?")
        self.assertEqual(session.ai_response_text, "The capital of France is Paris.")
        self.assertEqual(session.response_audio_path, "media/voice_responses/abc123.mp3")
        self.assertEqual(session.status, VoiceSession.Status.COMPLETED)

    @mock.patch("apps.voice.services.transcribe_audio._call_whisper")
    @mock.patch("apps.voice.services.generate_response._call_chat")
    @mock.patch("apps.voice.services.synthesize_speech._call_tts")
    def test_process_voice_message_case_2(
        self,
        mock_call_tts: Mock,
        mock_call_chat: Mock,
        mock_call_whisper: Mock,
    ):
        """
        Case: Each successful pipeline run creates a new independent VoiceSession
        Expected: Two requests produce two separate sessions in the DB
        """
        mock_call_whisper.return_value = "Hello"
        mock_call_chat.return_value = "Hi there!"
        mock_call_tts.return_value = "media/voice_responses/first.mp3"

        self.client.post(
            "/api/v1/voice/process/",
            {"audio": self._make_audio_file()},
            format="multipart",
        )

        mock_call_whisper.return_value = "Goodbye"
        mock_call_chat.return_value = "See you later!"
        mock_call_tts.return_value = "media/voice_responses/second.mp3"

        self.client.post(
            "/api/v1/voice/process/",
            {"audio": self._make_audio_file()},
            format="multipart",
        )

        self.assertEqual(VoiceSession.objects.count(), 2)

    # ------------------------------------------------------------------ #
    # Failure cases                                                        #
    # ------------------------------------------------------------------ #

    def test_process_voice_message_case_3(self):
        """
        Case: No audio file provided in request
        Expected: 400, no VoiceSession created
        """
        response = self.client.post(
            "/api/v1/voice/process/",
            {},
            format="multipart",
        )

        self.assertEqual(response.status_code, 400, response.data)
        self.assertEqual(VoiceSession.objects.count(), 0)

    def test_process_voice_message_case_4(self):
        """
        Case: Unsupported file type submitted
        Expected: 502, VoiceSession saved with status=FAILED
        """
        bad_file = SimpleUploadedFile(
            name="test.txt",
            content=b"not audio",
            content_type="text/plain",
        )
        response = self.client.post(
            "/api/v1/voice/process/",
            {"audio": bad_file},
            format="multipart",
        )

        self.assertEqual(response.status_code, 502, response.data)
        self.assertEqual(VoiceSession.objects.count(), 1)
        session = VoiceSession.objects.first()
        self.assertEqual(session.status, VoiceSession.Status.FAILED)

    @mock.patch("apps.voice.services.transcribe_audio._call_whisper")
    def test_process_voice_message_case_5(self, mock_call_whisper: Mock):
        """
        Case: Whisper transcription fails mid-pipeline
        Expected: 502, VoiceSession saved with status=FAILED
        """
        from apps.core.exceptions import TranscriptionFailedError
        mock_call_whisper.side_effect = TranscriptionFailedError("Whisper unavailable")

        response = self.client.post(
            "/api/v1/voice/process/",
            {"audio": self._make_audio_file()},
            format="multipart",
        )

        self.assertEqual(response.status_code, 502, response.data)
        session = VoiceSession.objects.first()
        self.assertEqual(session.status, VoiceSession.Status.FAILED)
        self.assertEqual(session.transcribed_text, "")

    @mock.patch("apps.voice.services.transcribe_audio._call_whisper")
    @mock.patch("apps.voice.services.generate_response._call_chat")
    def test_process_voice_message_case_6(
        self,
        mock_call_chat: Mock,
        mock_call_whisper: Mock,
    ):
        """
        Case: ChatGPT fails after transcription succeeds
        Expected: 502, VoiceSession saved with status=FAILED,
                  transcribed_text persisted, ai_response_text empty
        """
        from apps.core.exceptions import ResponseGenerationFailedError
        mock_call_whisper.return_value = "Tell me a joke"
        mock_call_chat.side_effect = ResponseGenerationFailedError("ChatGPT unavailable")

        response = self.client.post(
            "/api/v1/voice/process/",
            {"audio": self._make_audio_file()},
            format="multipart",
        )

        self.assertEqual(response.status_code, 502, response.data)
        session = VoiceSession.objects.first()
        self.assertEqual(session.status, VoiceSession.Status.FAILED)
        self.assertEqual(session.transcribed_text, "Tell me a joke")
        self.assertEqual(session.ai_response_text, "")

    @mock.patch("apps.voice.services.transcribe_audio._call_whisper")
    @mock.patch("apps.voice.services.generate_response._call_chat")
    @mock.patch("apps.voice.services.synthesize_speech._call_tts")
    def test_process_voice_message_case_7(
        self,
        mock_call_tts: Mock,
        mock_call_chat: Mock,
        mock_call_whisper: Mock,
    ):
        """
        Case: TTS fails after transcription and AI response both succeed
        Expected: 502, VoiceSession saved with status=FAILED,
                  transcribed_text and ai_response_text both persisted
        """
        from apps.core.exceptions import SpeechSynthesisFailedError
        mock_call_whisper.return_value = "How are you?"
        mock_call_chat.return_value = "I am doing great, thanks!"
        mock_call_tts.side_effect = SpeechSynthesisFailedError("TTS unavailable")

        response = self.client.post(
            "/api/v1/voice/process/",
            {"audio": self._make_audio_file()},
            format="multipart",
        )

        self.assertEqual(response.status_code, 502, response.data)
        session = VoiceSession.objects.first()
        self.assertEqual(session.status, VoiceSession.Status.FAILED)
        self.assertEqual(session.transcribed_text, "How are you?")
        self.assertEqual(session.ai_response_text, "I am doing great, thanks!")
        self.assertEqual(session.response_audio_path, "")
