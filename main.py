import whisper
import imageio_ffmpeg as ffmpeg
import os

os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg.get_ffmpeg_exe())
# ---------------------------
# Lazy Load Whisper Model
# ---------------------------
_model = None

def get_model():
    global _model
    if _model is None:
        _model = whisper.load_model("base")
    return _model


# ---------------------------
# SPEECH TO TEXT
# ---------------------------
def transcribe_audio(audio_path: str) -> str:
    try:
        model = get_model()
        result = model.transcribe(audio_path)
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Transcription Error: {e}")
        return ""


# ---------------------------
# GENERATE NOTES
# ---------------------------
def generate_notes(transcript: str) -> str:
    if not transcript or not transcript.strip():
        return "No transcript available to generate notes."

    return (
        "### 📘 Lecture Notes\n\n"
        f"{transcript}\n\n"
        "### 🔑 Key Takeaways\n"
        "- The lecture discusses important programming concepts.\n"
        "- Core ideas and examples are explained clearly.\n"
        "- Practical implementation is emphasized.\n"
    )


# ---------------------------
# GENERATE QUIZ
# ---------------------------
def generate_quiz(transcript: str) -> str:
    if not transcript or not transcript.strip():
        return "No transcript available to build a quiz."

    return (
        "### 📝 Quiz\n\n"
        "1. What is the main idea of the lecture?\n"
        "A) Concept explanation\n"
        "B) Random topic\n"
        "C) Irrelevant subject\n"
        "D) None of the above\n\n"
        "2. What key concept was emphasized?\n"
        "A) Core programming logic\n"
        "B) Entertainment\n"
        "C) Sports\n"
        "D) Politics\n\n"
        "3. Why is this concept important?\n"
        "A) Improves understanding\n"
        "B) Not useful\n"
        "C) Just theory\n"
        "D) No reason\n"
    )


# ---------------------------
# GENERATE FLASHCARDS
# ---------------------------
def generate_flashcards(transcript: str) -> str:
    if not transcript or not transcript.strip():
        return "No transcript available to build flashcards."

    return (
        "Q: What is the main topic of the lecture?\n"
        "A: The lecture explains key programming concepts.\n\n"
        "Q: Why is the concept important?\n"
        "A: It helps build strong foundational knowledge.\n\n"
        "Q: What should students focus on?\n"
        "A: Understanding the logic and practical application."
    )