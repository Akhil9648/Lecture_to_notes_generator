import streamlit as st
import os
from main  import transcribe_audio, generate_notes, generate_quiz, generate_flashcards

st.set_page_config(page_title="Lecture Voice to Notes Generator", layout="wide")

st.title("🎙 Lecture Voice to Notes Generator")
st.write("Upload your lecture audio and generate Notes, Quiz, or Flashcards instantly.")

# ----------------------------
# File Upload
# ----------------------------
uploaded_file = st.file_uploader("Upload Lecture Audio (.mp3 or .wav)", type=["mp3", "wav"])

if uploaded_file is not None:

    # Save file temporarily
    with open("temp_audio.wav", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Audio uploaded successfully.")
    st.audio("temp_audio.wav")

    # Transcribe
    with st.spinner("Transcribing audio... Please wait ⏳"):
        transcript = transcribe_audio("temp_audio.wav")

    st.subheader("Transcript")
    st.write(transcript)

    st.divider()

    st.subheader("Choose Action")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Generate Notes"):
            with st.spinner("Generating Notes..."):
                notes = generate_notes(transcript)
            st.markdown(notes)

    with col2:
        if st.button("Generate Quiz"):
            with st.spinner("Generating Quiz..."):
                quiz = generate_quiz(transcript)
            st.markdown(quiz)

    with col3:
        if st.button("Generate Flashcards"):
            with st.spinner("Generating Flashcards..."):
                flashcards = generate_flashcards(transcript)

            st.subheader("Flashcards")

            # Format flashcards nicely
            cards = flashcards.split("\n\n")
            for card in cards:
                if "Q:" in card and "A:" in card:
                    question = card.split("A:")[0].replace("Q:", "").strip()
                    answer = card.split("A:")[1].strip()

                    with st.expander(f"📌 {question}"):
                        st.write(answer)

st.markdown("---")
st.caption("Built by Lecture to Voice Team 🚀")
