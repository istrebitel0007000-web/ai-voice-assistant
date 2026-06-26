from unittest import mock
from unittest.mock import Mock

from rest_framework.test import APITestCase


class TestGenerateResponse(APITestCase):
    fixtures = []

    # ------------------------------------------------------------------ #
    # Success cases                                                        #
    # ------------------------------------------------------------------ #

    @mock.patch("apps.voice.services.generate_response._call_chat")
    def test_generate_response_case_1(self, mock_call_chat: Mock):
        """
        Case: Valid user text is submitted
        Expected: 200, ai_response_text returned in response
        """
        mock_call_chat.return_value = "The weather in Tashkent is sunny today."

        response = self.client.post(
            "/api/v1/voice/generate-response/",
            {"user_text": "What is the weather in Tashkent?"},
            format="json",
        )

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(
            response.data["ai_response_text"],
            "The weather in Tashkent is sunny today.",
        )
        mock_call_chat.assert_called_once_with("What is the weather in Tashkent?")

    @mock.patch("apps.voice.services.generate_response._call_chat")
    def test_generate_response_case_2(self, mock_call_chat: Mock):
        """
        Case: User text is a short greeting
        Expected: 200, ai_response_text returned
        """
        mock_call_chat.return_value = "Hello! How can I help you today?"

        response = self.client.post(
            "/api/v1/voice/generate-response/",
            {"user_text": "Hello"},
            format="json",
        )

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(
            response.data["ai_response_text"],
            "Hello! How can I help you today?",
        )

    # ------------------------------------------------------------------ #
    # Failure cases                                                        #
    # ------------------------------------------------------------------ #

    def test_generate_response_case_3(self):
        """
        Case: user_text field is missing from request body
        Expected: 400 bad request
        """
        response = self.client.post(
            "/api/v1/voice/generate-response/",
            {},
            format="json",
        )

        self.assertEqual(response.status_code, 400, response.data)

    def test_generate_response_case_4(self):
        """
        Case: user_text is an empty string
        Expected: 400 bad request — DRF CharField rejects blank before service runs
        """
        response = self.client.post(
            "/api/v1/voice/generate-response/",
            {"user_text": ""},
            format="json",
        )

        self.assertEqual(response.status_code, 400, response.data)

    @mock.patch("apps.voice.services.generate_response._call_chat")
    def test_generate_response_case_5(self, mock_call_chat: Mock):
        """
        Case: OpenAI Chat API is unavailable (external call fails)
        Expected: 502, response_generation_failed error code
        """
        from apps.core.exceptions import ResponseGenerationFailedError
        mock_call_chat.side_effect = ResponseGenerationFailedError("API unavailable")

        response = self.client.post(
            "/api/v1/voice/generate-response/",
            {"user_text": "Tell me a joke"},
            format="json",
        )

        self.assertEqual(response.status_code, 502, response.data)
