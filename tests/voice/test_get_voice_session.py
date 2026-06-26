from rest_framework.test import APITestCase

from apps.voice.models import VoiceSession


class TestGetVoiceSession(APITestCase):
    fixtures = [
        "tests/voice/fixtures/test_get_voice_session/voice_session.json",
    ]

    # ------------------------------------------------------------------ #
    # Success cases                                                        #
    # ------------------------------------------------------------------ #

    def test_get_voice_session_case_1(self):
        """
        Case: Valid session_id for an existing completed session
        Expected: 200, all session fields returned correctly
        """
        response = self.client.get("/api/v1/voice/sessions/1/detail/")

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["session_id"], 1)
        self.assertEqual(response.data["transcribed_text"], "What is the capital of France?")
        self.assertEqual(response.data["ai_response_text"], "The capital of France is Paris.")
        self.assertEqual(response.data["response_audio_path"], "media/voice_responses/abc123.mp3")
        self.assertEqual(response.data["status"], VoiceSession.Status.COMPLETED)

    # ------------------------------------------------------------------ #
    # Failure cases                                                        #
    # ------------------------------------------------------------------ #

    def test_get_voice_session_case_2(self):
        """
        Case: session_id does not exist in the database
        Expected: 404 not found
        """
        response = self.client.get("/api/v1/voice/sessions/9999/detail/")

        self.assertEqual(response.status_code, 404, response.data)

    def test_get_voice_session_case_3(self):
        """
        Case: session_id is zero (invalid value)
        Expected: 404 not found
        """
        response = self.client.get("/api/v1/voice/sessions/0/detail/")

        self.assertEqual(response.status_code, 404, response.data)
