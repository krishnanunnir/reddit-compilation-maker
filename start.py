import praw
import urllib.request
import os

reddit = praw.Reddit(client_id=os.environ["client_id"],
                     client_secret=os.environ["client_secret"],
                     user_agent=os.environ["user_agent")
print(reddit.read_only)
subredditW = reddit.subreddit("watchpeopledieinside")
for submission in subredditW.top(limit=5):
    video_url = submission.media["reddit_video"]["fallback_url"]
    audio_url = video_url.split("DASH_")[0] + "audio"
    urllib.request.urlretrieve(video_url, "temp/" + submission.title+".mp4")
    urllib.request.urlretrieve(audio_url, "temp/" + submission.title+".mp3")