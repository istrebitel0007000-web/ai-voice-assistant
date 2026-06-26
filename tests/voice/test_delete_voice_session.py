from rest_framework.test import APITestCase

from apps.voice.models import VoiceSession


class TestDeleteVoiceSession(APITestCase):
    fixtures = [
        "tests/voice/fixtures/test_delete_voice_session/voice_session.json",
    ]

    # ------------------------------------------------------------------ #
    # Success cases                                                        #
    # ------------------------------------------------------------------ #

    def test_delete_voice_session_case_1(self):
        """
        Case: Valid session_id for an existing session
        Expected: 204 No Content, session removed from DB
        """
        response = self.client.delete("/api/v1/voice/sessions/1/delete/")

        self.assertEqual(response.status_code, 204, response)
        self.assertFalse(VoiceSession.objects.filter(id=1).exists())

    def test_delete_voice_session_case_2(self):
        """
        Case: Deleting session with pk=1 must not affect session with pk=2
        Expected: 204, only pk=1 is removed, pk=2 still exists in DB
        """
        self.client.delete("/api/v1/voice/sessions/1/delete/")

        self.assertFalse(VoiceSession.objects.filter(id=1).exists())
        self.assertTrue(VoiceSession.objects.filter(id=2).exists())

    # ------------------------------------------------------------------ #
    # Failure cases                                                        #
    # ------------------------------------------------------------------ #

    def test_delete_voice_session_case_3(self):
        """
        Case: session_id does not exist in the database
        Expected: 404 Not Found, no sessions deleted
        """
        response = self.client.delete("/api/v1/voice/sessions/9999/delete/")

        self.assertEqual(response.status_code, 404, response)
        self.assertEqual(VoiceSession.objects.count(), 2)

    def test_delete_voice_session_case_4(self):
        """
        Case: session_id is zero (invalid value, no session has pk=0)
        Expected: 404 Not Found
        """
        response = self.client.delete("/api/v1/voice/sessions/0/delete/")

        self.assertEqual(response.status_code, 404, response)
        self.assertEqual(VoiceSession.objects.count(), 2)
