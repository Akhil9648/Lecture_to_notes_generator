import streamlit as st
import tempfile
import os
from main import transcribe_audio, generate_notes, generate_quiz, generate_flashcards

st.set_page_config(page_title="Lecture Voice to Notes Generator", layout="wide")

st.title("🎙 Lecture Voice to Notes Generator")
st.write("Upload your lecture audio and generate Notes, Quiz, or Flashcards instantly.")

# ----------------------------
# Session State Initialization
# ----------------------------
if "transcript" not in st.session_state:
    st.session_state.transcript = None

# ----------------------------
# File Upload
# ----------------------------
uploaded_file = st.file_uploader(
    "Upload Lecture Audio (.mp3 or .wav)",
    type=["mp3", "wav"]
)

if uploaded_file is not None:

    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        temp_audio_file.write(uploaded_file.getbuffer())
        temp_audio_path = temp_audio_file.name

    st.success("Audio uploaded successfully.")
    st.audio(temp_audio_path)

    # Transcribe
    with st.spinner("Transcribing audio... Please wait ⏳"):
        transcript = transcribe_audio(temp_audio_path)

    # Delete temp file after transcription
    try:
        os.remove(temp_audio_path)
    except Exception:
        pass

    if not transcript:
        st.error("Transcription failed. Please check your audio file.")
        st.stop()

    st.session_state.transcript = transcript

# ----------------------------
# Display Transcript
# ----------------------------
if st.session_state.transcript:
    st.subheader("Transcript")
    st.write(st.session_state.transcript)

    st.divider()
    st.subheader("Choose Action")

    col1, col2, col3 = st.columns(3)

    # ----------------------------
    # Generate Notes
    # ----------------------------
    with col1:
        if st.button("Generate Notes"):
            with st.spinner("Generating Notes..."):
                notes = generate_notes(st.session_state.transcript)
            st.markdown(notes)

    # ----------------------------
    # Generate Quiz
    # ----------------------------
    with col2:
        if st.button("Generate Quiz"):
            with st.spinner("Generating Quiz..."):
                quiz = generate_quiz(st.session_state.transcript)
            st.markdown(quiz)

    # ----------------------------
    # Generate Flashcards
    # ----------------------------
    with col3:
        if st.button("Generate Flashcards"):
            with st.spinner("Generating Flashcards..."):
                flashcards = generate_flashcards(st.session_state.transcript)

            if "Q:" not in flashcards:
                st.warning(flashcards)
            else:
                st.subheader("Flashcards")
                cards = flashcards.split("\n\n")

                for card in cards:
                    if "Q:" in card and "A:" in card:
                        question = card.split("A:")[0].replace("Q:", "").strip()
                        answer = card.split("A:")[1].strip()

                        with st.expander(f"📌 {question}"):
                            st.write(answer)

st.markdown("---")
st.caption("Built by Lecture to Voice Team 🚀")