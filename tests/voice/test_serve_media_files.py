import os
import importlib

from django.test import TestCase, override_settings
from django.conf import settings
from django.urls import clear_url_caches


class TestServeMediaFiles(TestCase):
    """
    Regression test for a production bug where MEDIA_URL/MEDIA_ROOT
    were defined in settings.py but never wired into urlpatterns,
    causing every generated audio file to 404 when the frontend
    tried to play it back — breaking the final step of the voice
    pipeline (hearing the AI's spoken reply).

    Note: Django's test runner forces DEBUG=False by default
    (this is intentional Django behavior, separate from our fix).
    Since our fix in config/urls.py is guarded by `if settings.DEBUG`,
    we must explicitly override DEBUG=True here and force urlpatterns
    to re-evaluate, to correctly simulate the real `runserver` environment.
    """

    def setUp(self):
        self.test_dir = os.path.join(settings.MEDIA_ROOT, "voice_responses")
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_file_path = os.path.join(self.test_dir, "test_regression.mp3")
        with open(self.test_file_path, "wb") as f:
            f.write(b"fake-mp3-bytes-for-testing")

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    @override_settings(ALLOWED_HOSTS=["testserver"], DEBUG=True)
    def test_serve_media_files_case_1(self):
        """
        Case: A generated audio file exists on disk under MEDIA_ROOT,
              simulating the real `runserver` environment (DEBUG=True)
        Expected: 200, file is served with correct bytes
        """
        import config.urls
        importlib.reload(config.urls)
        clear_url_caches()

        response = self.client.get("/media/voice_responses/test_regression.mp3")

        self.assertEqual(response.status_code, 200)
        content = b"".join(response.streaming_content)
        self.assertEqual(content, b"fake-mp3-bytes-for-testing")

        # Restore urlpatterns to the test-runner default (DEBUG=False)
        # so this test doesn't leak state into other tests.
        importlib.reload(config.urls)
        clear_url_caches()

    @override_settings(ALLOWED_HOSTS=["testserver"], DEBUG=True)
    def test_serve_media_files_case_2(self):
        """
        Case: Requested media file does not exist on disk,
              simulating the real `runserver` environment (DEBUG=True)
        Expected: 404 not found (correct behavior, not a silent failure)
        """
        import config.urls
        importlib.reload(config.urls)
        clear_url_caches()

        response = self.client.get("/media/voice_responses/does-not-exist.mp3")

        self.assertEqual(response.status_code, 404)

        importlib.reload(config.urls)
        clear_url_caches()
