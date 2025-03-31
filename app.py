import streamlit as st
import whisper
import ffmpeg
import pandas as pd
import pickle
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from chromadb import Client
from chromadb.config import Settings

embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_audio(uploaded_file):
    audio_path = "temp_audio.wav"
    temp_file = f"temp_{uploaded_file.name}"
    with open(temp_file, "wb") as f:
        f.write(uploaded_file.getvalue())

    try:
        if uploaded_file.name.endswith(('.mp4', '.mkv')):
            ffmpeg.input(temp_file).output(audio_path).run(overwrite_output=True)
        else:
            audio_path = temp_file
        return audio_path, temp_file
    except Exception as e:
        st.error(f"Error extracting audio: {str(e)}")
        return None, None

def transcribe_audio(audio_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)

        subtitles = []
        for i, segment in enumerate(result['segments']):
            start_time = format_timestamp(segment['start'])
            end_time = format_timestamp(segment['end'])
            text = segment['text']
            subtitles.append(f"{i + 1}\n{start_time} --> {end_time}\n{text}\n")
        
        return subtitles
    except Exception as e:
        st.error(f"Error during transcription: {str(e)}")
        return []

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def embed_subtitles(subtitles):
    raw_texts = [line.split('\n')[2] for line in subtitles if line.strip()]
    embeddings = embed_model.encode(raw_texts)

    df = pd.DataFrame({
        'subtitle': raw_texts,
        'embedding': list(embeddings)
    })

    with open('subtitle_embeddings.pkl', 'wb') as f:
        pickle.dump(df, f)

    return df

def save_to_chroma(embeddings):
    client = Client(Settings())
    collection = client.create_collection(name="subtitles")

    for idx, row in embeddings.iterrows():
        collection.add(
            documents=[row['subtitle']],
            ids=[str(idx)],
            embeddings=[row['embedding']]
        )
    return collection

def search_subtitles(query, collection):
    try:
        results = collection.query(query_texts=[query], n_results=5)
        return results['documents']
    except Exception as e:
        st.error(f"Error searching subtitles: {str(e)}")
        return []

def main():
    st.set_page_config(page_title="Video/Audio Subtitle Generator", layout="wide")
    st.title("🎥🎵 Video/Audio Subtitle Generator")

    with st.sidebar:
        uploaded_file = st.file_uploader("Upload Video/Audio", type=["mp4", "mkv", "mp3", "wav"])
        query = st.text_input("Search Subtitles")
        download_btn = st.button("Download Subtitles")

    if uploaded_file:
        with st.spinner("Extracting audio..."):
            audio_path, temp_file = extract_audio(uploaded_file)

        if audio_path:
            with st.spinner("Generating subtitles..."):
                subtitles = transcribe_audio(audio_path)
                st.success("Subtitles Generated!")

            if uploaded_file.name.endswith(('.mp4', '.mkv')):
                st.video(uploaded_file)
            else:
                st.audio(uploaded_file)

            st.write("### Generated Subtitles:")
            for sub in subtitles:
                st.text(sub)

            with st.spinner("Embedding and storing subtitles..."):
                embeddings = embed_subtitles(subtitles)
                
                if embeddings.empty:
                    st.warning("No subtitles generated.")
                else:
                    collection = save_to_chroma(embeddings)

            if query:
                results = search_subtitles(query, collection)
                st.write("### Matching Subtitles:")
                if results:
                    for idx, sub in enumerate(results, start=1):
                        st.write(f"{idx}. {sub}")
                else:
                    st.warning("No matching subtitles found.")

            if download_btn:
                with open("generated_subtitles.srt", "w") as f:
                    f.writelines(subtitles)

                with open("generated_subtitles.srt", "rb") as f:
                    st.download_button("Download SRT", f, file_name="generated_subtitles.srt", mime="text/plain")

if __name__ == '__main__':
    main() 
