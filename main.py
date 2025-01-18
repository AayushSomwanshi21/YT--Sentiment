import googleapiclient.discovery
from transformers import pipeline
import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_service_name = "youtube"
api_version = "v3"

sentiment_analysis = pipeline("sentiment-analysis")

# Fetching the youtube comments using next_page_token
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=os.environ.get("DEVELOPER_KEY")
)


def fetch_all_comments(video_id, max_comments=500):
    comments_data = []
    next_page_token = None

    while len(comments_data) < max_comments:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            order="relevance",
            pageToken=next_page_token
        )
        response = request.execute()

        # comments and likes counts
        comments_data.extend([
            {
                'comment': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                'likeCount': item['snippet']['topLevelComment']['snippet']['likeCount']
            }
            for item in response['items']
        ])

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return comments_data[:max_comments]


def truncate_comments(comment, max_len=512):

    return comment[:max_len]


@app.get("/")
async def read_root(id: str = Query(...)):

    video_id = id
    all_comments = fetch_all_comments(video_id, max_comments=500)

    sorted_comments = sorted(
        all_comments, key=lambda x: x['likeCount'], reverse=True)
    top_comments = sorted_comments[:100]

    batch_size = 20
    comments = [truncate_comments(data['comment']) for data in top_comments]
    batches = [comments[i: i + batch_size]
               for i in range(0, len(comments), batch_size)]

    positive_count = 0
    negative_count = 0
    total_score = 0

    for batch in batches:
        results = sentiment_analysis(batch)
        for result in results:
            sentiment_label = result['label']
            sentiment_score = result['score']
            if sentiment_label == "POSITIVE":
                positive_count += 1
            else:
                negative_count += 1
            total_score += sentiment_score

    average_score = total_score / len(top_comments) if top_comments else 0
    overall_sentiment = "POSITIVE" if positive_count > negative_count else "NEGATIVE"

    return {
        "positive_comments": positive_count,
        "negative_comments": negative_count,
        "average_sentiment_score": round(average_score, 4),
        "overall_sentiment": overall_sentiment,
    }
