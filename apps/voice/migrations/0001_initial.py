from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="VoiceSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_audio_path", models.CharField(max_length=512)),
                ("transcribed_text", models.TextField(blank=True, default="")),
                ("ai_response_text", models.TextField(blank=True, default="")),
                (
                    "response_audio_path",
                    models.CharField(blank=True, default="", max_length=512),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "voice_session",
                "ordering": ["-created_at"],
            },
        ),
    ]
