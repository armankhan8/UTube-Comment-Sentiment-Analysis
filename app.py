from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from googleapiclient.discovery import build
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import os
from dotenv import load_dotenv
import re

# Download required NLTK data
nltk.download('vader_lexicon')

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))

# Initialize VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    video_id = None
    if 'youtube.com' in url:
        # Handle URLs with additional parameters
        video_id = re.search(r'v=([^&?]+)', url)
        if video_id:
            video_id = video_id.group(1)
    elif 'youtu.be' in url:
        # Handle shortened URLs with additional parameters
        video_id = url.split('/')[-1].split('?')[0]
    return video_id

def get_video_comments(video_id):
    """Fetch comments from YouTube video."""
    comments = []
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=100
    )
    
    while request and len(comments) < 100:
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        
        request = youtube.commentThreads().list_next(request, response)
    
    return comments

def analyze_sentiment(comments):
    """Analyze sentiment of comments using VADER."""
    results = {
        'positive': 0,
        'negative': 0,
        'neutral': 0,
        'total': len(comments),
        'samples': []  # Add samples of analyzed comments
    }
    
    for comment in comments:
        sentiment = sia.polarity_scores(comment)
        sentiment_label = 'neutral'
        if sentiment['compound'] >= 0.1:  # Increased threshold for positive
            results['positive'] += 1
            sentiment_label = 'positive'
        elif sentiment['compound'] <= -0.1:  # Increased threshold for negative
            results['negative'] += 1
            sentiment_label = 'negative'
        else:
            results['neutral'] += 1
            
        # Add sample comments (up to 5 for each sentiment)
        if len([s for s in results['samples'] if s['sentiment'] == sentiment_label]) < 5:
            results['samples'].append({
                'text': comment,
                'sentiment': sentiment_label,
                'score': sentiment['compound']
            })
    
    return results

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_video():
    try:
        data = request.get_json()
        video_url = data.get('url')
        
        if not video_url:
            return jsonify({'error': 'Please enter a YouTube video URL'}), 400
        
        video_id = extract_video_id(video_url)
        if not video_id:
            return jsonify({'error': 'Invalid YouTube URL. Please enter a valid YouTube video URL'}), 400
        
        try:
            comments = get_video_comments(video_id)
        except Exception as e:
            if 'videoNotFound' in str(e):
                return jsonify({'error': 'Video not found. Please check the URL and try again'}), 404
            elif 'commentsDisabled' in str(e):
                return jsonify({'error': 'Comments are disabled for this video'}), 403
            else:
                return jsonify({'error': 'Failed to fetch comments. Please try again later'}), 500
        
        if not comments:
            return jsonify({'error': 'No comments found for this video'}), 404
        
        sentiment_results = analyze_sentiment(comments)
        return jsonify(sentiment_results)
    
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred. Please try again later'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) 