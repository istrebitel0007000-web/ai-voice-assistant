# AI Voice Assistant

A Django REST Framework API that accepts audio input and returns an AI-generated spoken response.

**Pipeline:** Upload audio → Whisper transcribes it → GPT-4o-mini generates a reply → TTS converts it to speech → MP3 saved to disk.

---

## Tech Stack

- Python 3.9
- Django 4.2
- Django REST Framework 3.14
- OpenAI API (Whisper, GPT-4o-mini, TTS)

---

## Project Structure

```
voice_assistant/
├── apps/
│   ├── core/
│   │   ├── serializer.py       # Base serializer all serializers inherit from
│   │   └── exceptions.py       # Custom API exceptions
│   └── voice/
│       ├── models/             # VoiceSession model
│       ├── services/           # All business logic (one file per action)
│       ├── views/              # HTTP handlers (one file per endpoint)
│       ├── migrations/         # DB migrations
│       └── urls.py             # Voice app URL config
├── config/
│   ├── settings.py
│   └── urls.py
├── tests/
│   └── voice/
│       ├── fixtures/           # One fixture folder per test file
│       └── test_*.py           # One test file per feature
├── requirements.txt
├── manage.py
└── .env.example
```

---

## Local Setup

### 1. Clone and enter the project

```bash
cd voice_assistant
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Mac / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your `.env` file

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
OPENAI_API_KEY=your-openai-api-key-here
```

Get your OpenAI API key from: https://platform.openai.com/api-keys

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Run tests

```bash
python manage.py test tests/
```

Expected output:
```
Ran 36 tests in X.XXXs
OK
```

### 7. Start the server

```bash
python manage.py runserver
```

Server runs at: http://127.0.0.1:8000

---

## API Endpoints

All endpoints are prefixed with `/api/v1/voice/`.

### Full Pipeline (main endpoint)

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/v1/voice/process/` | Upload audio → get AI voice response |

**Request:** `multipart/form-data`
```
audio: <audio file>   # WAV, MP3, WebM, MP4, OGG
```

**Response:** `200 OK`
```json
{
  "session_id": 1,
  "transcribed_text": "What is the capital of France?",
  "ai_response_text": "The capital of France is Paris.",
  "response_audio_path": "media/voice_responses/abc123.mp3",
  "status": "completed"
}
```

---

### Individual AI Steps (Week 1)

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/v1/voice/transcribe/` | Audio file → transcribed text |
| POST | `/api/v1/voice/generate-response/` | Text → AI reply text |
| POST | `/api/v1/voice/synthesize-speech/` | Text → MP3 audio file path |

---

### Session Management

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/v1/voice/sessions/list/` | List all sessions |
| GET | `/api/v1/voice/sessions/{id}/detail/` | Get one session |
| DELETE | `/api/v1/voice/sessions/{id}/delete/` | Delete one session |
| DELETE | `/api/v1/voice/sessions/delete-all/` | Delete all sessions |

---

## Error Responses

| Status | Code | Meaning |
|--------|------|---------|
| 400 | — | Missing or invalid request field |
| 404 | `voice_session_not_found` | Session ID does not exist |
| 502 | `transcription_failed` | Whisper API error |
| 502 | `response_generation_failed` | ChatGPT API error |
| 502 | `speech_synthesis_failed` | TTS API error |

---

## Running Tests

Run all tests:
```bash
python manage.py test tests/
```

Run a specific test file:
```bash
python manage.py test tests.voice.test_process_voice_message
```

Run a specific test case:
```bash
python manage.py test tests.voice.test_process_voice_message.TestProcessVoiceMessage.test_process_voice_message_case_1
```

---

## Coding Standards

This project follows strict TMS mono coding standards. See `SKILL.md` for full details. Key rules:

- Views handle HTTP only — no business logic
- All logic lives in services (one file, one responsibility)
- Serializers inherit from `apps.core.serializer.Serializer`
- Tests: one file per feature, `case_N` naming, dedicated fixtures, literals in asserts
- Mock only external calls (OpenAI API)
