from django.urls import path

from apps.voice.views import (
    TranscribeAudioView,
    GenerateResponseView,
    SynthesizeSpeechView,
    ProcessVoiceMessageView,
    GetVoiceSessionView,
    ListVoiceSessionsView,
    DeleteVoiceSessionView,
    DeleteAllVoiceSessionsView,
)

urlpatterns = [
    # Individual AI step endpoints (Week 1)
    path("transcribe/", TranscribeAudioView.as_view(), name="voice-transcribe"),
    path("generate-response/", GenerateResponseView.as_view(), name="voice-generate-response"),
    path("synthesize-speech/", SynthesizeSpeechView.as_view(), name="voice-synthesize-speech"),

    # Full pipeline endpoint (Week 2)
    path("process/", ProcessVoiceMessageView.as_view(), name="voice-process"),

    # Session management endpoints (Week 2 & 3)
    path("sessions/list/", ListVoiceSessionsView.as_view(), name="voice-session-list"),
    path("sessions/delete-all/", DeleteAllVoiceSessionsView.as_view(), name="voice-session-delete-all"),
    path("sessions/<int:session_id>/detail/", GetVoiceSessionView.as_view(), name="voice-session-detail"),
    path("sessions/<int:session_id>/delete/", DeleteVoiceSessionView.as_view(), name="voice-session-delete"),
]
