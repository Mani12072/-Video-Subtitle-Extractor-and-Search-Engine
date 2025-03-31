# 🎥 **AI-Powered Video/Audio Subtitle Search Engine**

## 🚀 Project Description
This project is an **AI-powered application** that generates and searches subtitles from video/audio files.  
It uses **OpenAI's Whisper model** for speech-to-text transcription, **ChromaDB** for storing and searching subtitle embeddings, and **Streamlit** for an interactive web-based UI.  

---

## ⚙️ Tech Stack
✅ **Python Libraries:**  
- `whisper`: For audio transcription  
- `ffmpeg`: For audio extraction from video files  
- `pandas`: For handling subtitle data  
- `ChromaDB`: For storing and searching subtitle embeddings  
- `SentenceTransformers`: For creating embeddings  
- `Streamlit`: For building the UI  

✅ **File Formats Supported:**  
- **Input:** `.mp4`, `.mkv`, `.mp3`, `.wav`  
- **Output:** Subtitles in `.srt` format  

---

## 🔥 Key Features
1. **Audio Extraction:**  
   - Automatically extracts audio from video files (MP4, MKV) using `ffmpeg`.  

2. **Subtitle Generation:**  
   - Generates accurate subtitles using OpenAI's `whisper` model.  
   - Formats subtitles in `.srt` format with timestamps.  

3. **ChromaDB Integration:**  
   - Stores subtitles as embeddings in **ChromaDB** for efficient searching.  
   - Uses `PersistentClient` to ensure subtitle collections persist across sessions.  

4. **Semantic Search:**  
   - Allows users to search for specific phrases or dialogues in the subtitles.  
   - Displays the matching subtitles with context.  

5. **Downloadable Subtitles:**  
   - Users can download the generated subtitles in `.srt` format.  
