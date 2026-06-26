from rest_framework.test import APITestCase

from apps.voice.models import VoiceSession


class TestDeleteAllVoiceSessions(APITestCase):
    fixtures = [
        "tests/voice/fixtures/test_delete_all_voice_sessions/voice_session.json",
    ]

    # ------------------------------------------------------------------ #
    # Success cases                                                        #
    # ------------------------------------------------------------------ #

    def test_delete_all_voice_sessions_case_1(self):
        """
        Case: Two sessions exist, delete-all is called
        Expected: 200, deleted_count=2 returned, DB is empty
        """
        response = self.client.delete("/api/v1/voice/sessions/delete-all/")

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["deleted_count"], 2)
        self.assertEqual(VoiceSession.objects.count(), 0)

    def test_delete_all_voice_sessions_case_2(self):
        """
        Case: No sessions exist in the database (already empty)
        Expected: 200, deleted_count=0, no errors raised
        """
        VoiceSession.objects.all().delete()

        response = self.client.delete("/api/v1/voice/sessions/delete-all/")

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["deleted_count"], 0)
        self.assertEqual(VoiceSession.objects.count(), 0)
