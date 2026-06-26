from rest_framework.test import APITestCase

from apps.voice.models import VoiceSession


class TestListVoiceSessions(APITestCase):
    fixtures = [
        "tests/voice/fixtures/test_list_voice_sessions/voice_session.json",
    ]

    # ------------------------------------------------------------------ #
    # Success cases                                                        #
    # ------------------------------------------------------------------ #

    def test_list_voice_sessions_case_1(self):
        """
        Case: Two sessions exist in the database
        Expected: 200, both sessions returned in the response
        """
        response = self.client.get("/api/v1/voice/sessions/list/")

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(len(response.data), 2)

    def test_list_voice_sessions_case_2(self):
        """
        Case: Sessions are ordered by most recent first (model Meta ordering)
        Expected: 200, session with pk=2 (newer) appears before pk=1 (older)
        """
        response = self.client.get("/api/v1/voice/sessions/list/")

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data[0]["session_id"], 2)
        self.assertEqual(response.data[1]["session_id"], 1)

    def test_list_voice_sessions_case_3(self):
        """
        Case: Response contains correct field values for each session
        Expected: 200, first item (most recent) has correct transcribed_text and status
        """
        response = self.client.get("/api/v1/voice/sessions/list/")

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data[0]["transcribed_text"], "What time is it?")
        self.assertEqual(response.data[0]["status"], VoiceSession.Status.COMPLETED)

    # ------------------------------------------------------------------ #
    # Failure cases                                                        #
    # ------------------------------------------------------------------ #

    def test_list_voice_sessions_case_4(self):
        """
        Case: No sessions exist in the database
        Expected: 200, empty list returned (not a 404)
        """
        VoiceSession.objects.all().delete()

        response = self.client.get("/api/v1/voice/sessions/list/")

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.data, [])
