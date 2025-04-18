import googleapiclient.discovery
from transformers import pipeline
import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import html
import random

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

# fetching the youtube comments using next_page_token
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=os.environ.get("DEVELOPER_KEY")
)


def comments_summary(comments, max_tokens=1000, batch_size=5):

    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    random.shuffle(comments)

    # divide the comments into smaller chunks for batch processsing
    comments_chunks = [" ".join(comments[i: i + batch_size])
                       for i in range(0, len(comments), batch_size)]

    # find the partial summary of the chunks
    partial_summary = []

    for chunk in comments_chunks:

        chunk_tokens = len(chunk.split())

        max_len = min(chunk_tokens//2, 50)
        min_len = max(20, max_len // 2)

        summary = summarizer(
            chunk[:max_tokens], max_length=max_len, min_length=min_len, do_sample=False)
        partial_summary.append(summary[0]['summary_text'])

    # finalize the summary by generating the summary of the partial summary
    partial_joined = ' '.join(partial_summary)
    final_summary = summarizer(partial_joined[:max_tokens], max_length=50,
                               min_length=25, do_sample=False)

    return final_summary[0]['summary_text']


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


def video_info(video_id):

    req = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    res = req.execute()

    # extract thumbnail link
    thumbnails = res['items'][0]['snippet']['thumbnails']
    thumbnail_url = thumbnails.get('high', thumbnails.get(
        'medium', thumbnails.get('default'))).get('url')

    # extract title
    if 'items' in res and len(res['items']) > 0:
        title = res['items'][0]['snippet']['title']

    return title, thumbnail_url


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
    video_data, thumbnail_data = video_info(video_id)

    # summarize the comments

    summary = comments_summary(comments)
    new_summary = html.unescape(summary)
    '''
    summary_list = summary.split('.')
    final_summary = []

    for each_summary in summary_list:
        if each_summary.strip() != '':
            final_summary.append(html.unescape(each_summary.strip()))
    '''

    return {
        "positive_comments": positive_count,
        "negative_comments": negative_count,
        "average_sentiment_score": round(average_score, 4),
        "overall_sentiment": overall_sentiment,
        "video_name": video_data,
        "thumbnail_img": thumbnail_data,
        "summary_text": new_summary
    }
