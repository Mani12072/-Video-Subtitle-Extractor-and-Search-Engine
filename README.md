# **Video Subtitle Extraction and Search Project**

## **Project Overview**
This project extracts subtitles from uploaded video files and stores them in **Chroma DB** for efficient retrieval. It uses **OpenAI Whisper** for speech-to-text conversion and **cosine similarity** to search for relevant subtitles based on user queries.

---

## **Features**
- **Video Upload:** Users can upload video files through the Streamlit sidebar.
- **Subtitle Extraction:** The project uses **OpenAI Whisper** to transcribe the speech into text subtitles.
- **Subtitle Storage:** Extracted subtitles are stored in **Chroma DB** for efficient retrieval.
- **Search with Cosine Similarity:** Users can enter a query to search for relevant subtitles. The system uses **cosine similarity** to find and display the most relevant subtitle segments.
- **Permanent Storage:** Uploaded subtitles are stored permanently in Chroma DB for future retrieval.

---

## **Technologies Used**
- **Python**
- **Streamlit** (UI)
- **Whisper** (speech-to-text)
- **Chroma DB** (vector database for subtitle storage)
- **Cosine Similarity** (text matching)
- **NLP** (subtitle cleaning and preprocessing)

