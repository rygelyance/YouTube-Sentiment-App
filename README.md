# YouTube Sentiment Lens 🎥📊

A full-stack machine learning application that provides real-time sentiment analysis of YouTube video comments. This project demonstrates a complete data pipeline: from raw API ingestion to Natural Language Processing (NLP) inference and representative data extraction.

---

## 🚀 The Mission
The goal of this project is to move beyond static data science notebooks and provide a live, functional service. It allows users to gain an instant "pulse" on public opinion for any YouTube video by analyzing the most recent discourse.

---

## 🛠️ Tech Stack (Current Progress)
Backend: FastAPI (Python)

ML Engine: Hugging Face Transformers (RoBERTa-base)

Data Ingestion: YouTube Data API v3

Validation: Pydantic

---

## 🏗️ Technical Architecture & Pipeline
The pipeline follows a strict modular flow to ensure clean data processing:

Extraction: Utilizing a regex-based parser to handle multiple YouTube URL formats (Shorts, Desktop, Mobile) to extract the unique Video ID.

Ingestion: Interfacing with the YouTube Data API to fetch comment threads while managing API quotas and pagination.

NLP Inference: * Model Selection: Uses the twitter-roberta-base-sentiment model, a Transformer model optimized for social media text (slang, emojis, and sarcasm).

Optimization: Implements batch processing (Batch Size: 8) and token truncation to ensure high-speed inference without memory overflows.

Representative Sampling: Instead of just showing random comments, the system calculates the "Mean Sentiment Score" and uses distance-based matching to identify the specific comments that most accurately represent the overall consensus.

---

## 🧪 Current Features
[x] Universal URL Parsing: Robust handling of various YouTube link structures.

[x] Real-time Inference: Live sentiment classification (Positive/Negative/Neutral).

[x] Smart Sampling: Identification of comments that match the collective sentiment.

[x] Automated Documentation: Built-in API testing via FastAPI/Swagger UI at /docs.

📈 Next Steps
[ ] Containerization of the environment using Docker.

[ ] Developing a React frontend for an interactive user experience.

[ ] Implementing Asynchronous Task Queuing for handling large-scale comment sections.