from django.db import models


class VoiceSession(models.Model):
    """
    Stores each voice interaction: the transcribed user speech,
    the AI text response, and the path to the synthesized audio file.
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    user_audio_path = models.CharField(max_length=512)
    transcribed_text = models.TextField(blank=True, default="")
    ai_response_text = models.TextField(blank=True, default="")
    response_audio_path = models.CharField(max_length=512, blank=True, default="")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "voice_session"
        ordering = ["-created_at"]
