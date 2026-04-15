import os
import re
from fastapi import FastAPI, HTTPException
from googleapiclient.discovery import build
from pydantic import BaseModel
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch
import numpy as np

app = FastAPI()

# Replace with your actual API key for the YouTube Data API!
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", 'YOUR_API_KEY_HERE')
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

class AnalysisRequest(BaseModel):
    url: str

class SentimentAnalyzer:
    def __init__(self):
        # Using RoBERTa-base for sentiment
        self.model_path = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
        self.classifier = pipeline("sentiment-analysis", model=self.model, tokenizer=self.tokenizer)
        
        # Mapping for the model's output labels
        self.labels = {
            "negative": 0,
            "neutral": 1,
            "positive": 2
        }

    def analyze_batch(self, comments):
        if not comments:
            return "Neutral", []

        # 1. Run inference
        # We truncate to 512 tokens (max for BERT/RoBERTa) to prevent crashes
        results = self.classifier(comments, truncation=True, batch_size=8)
        
        # 2. Calculate average sentiment
        scores = [self.labels[res['label']] for res in results]
        avg_score = sum(scores) / len(scores)
        
        # Determine overall sentiment label
        if avg_score < 0.8: overall_label = "Negative"
        elif avg_score > 1.2: overall_label = "Positive"
        else: overall_label = "Neutral"

        # 3. Find the "most representative" comments
        # We look for comments whose individual score is closest to the average
        # For simplicity in this starter, we'll just grab the indices of those matching the label
        representative_comments = [
            comments[i] for i, res in enumerate(results) 
            if res['label'] == overall_label.lower()
        ][:3]

        return overall_label, representative_comments

def extract_video_id(url: str):
    """Extracts the 11-character YouTube video ID from various URL formats."""
    reg = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(reg, url)
    if not match:
        raise ValueError("Invalid YouTube URL")
    return match.group(1)

def fetch_youtube_comments(video_id: str, max_comments: int = 100):
    comments = []
    try:
        # Fetch top-level comment threads
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(max_comments, 100),
            textFormat="plainText"
        )
        response = request.execute()

        for item in response.get("items", []):
            comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment_text)
            
        return comments
    except Exception as e:
        print(f"Error fetching comments: {e}")
        return []
    
# Initialize the analyzer
analyzer = SentimentAnalyzer()

@app.post("/analyze")
async def analyze_video(request: AnalysisRequest):
    try:
        video_id = extract_video_id(request.url)
        comments = fetch_youtube_comments(video_id)
        
        if not comments:
            raise HTTPException(status_code=404, detail="No comments found or video unavailable.")

        # New ML Logic
        overall_sentiment, typical_comments = analyzer.analyze_batch(comments)

        return {
            "video_id": video_id,
            "comment_count": len(comments),
            "overall_sentiment": overall_sentiment,
            "representative_comments": typical_comments
        }
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")