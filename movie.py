import unicodedata
import praw
import urllib.request
from urllib.error import HTTPError
from moviepy.editor import *
import shutil
import os
import re

temp ="./temp/"
final ="./final/"
def clean_all():
    shutil.rmtree(temp, ignore_errors=True)
    shutil.rmtree(final, ignore_errors=True)
    os.makedirs(temp)
    os.makedirs(final)

# Copied shamelessly from django
def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)
def main():
    clean_all()
    reddit = praw.Reddit(client_id=os.environ["client_id"],
                        client_secret=os.environ["client_secret"],
                        user_agent=os.environ["user_agent"])
    final_clip = []
    subredditW = reddit.subreddit("watchpeopledieinside")
    for submission in subredditW.top(limit=5):
        video_url = submission.media["reddit_video"]["fallback_url"]
        audio_url = video_url.split("DASH_")[0] + "audio"
        escaped_title = get_valid_filename(submission.title)
        urllib.request.urlretrieve(video_url, "temp/" + escaped_title+".mp4")
        # Handling case of no audio as well
        try:
            urllib.request.urlretrieve(audio_url, "temp/" + escaped_title+".mp3")
            videoClip = VideoFileClip(temp+escaped_title+".mp4")
            videoClip = videoClip.set_audio(AudioFileClip(temp+escaped_title+".mp3"))
            final_clip.append(videoClip)
        except  HTTPError as ex:
            videoClip = VideoFileClip(temp+escaped_title+".mp4")
            final_clip.append(videoClip)
    final_video = concatenate_videoclips(final_clip,method='compose')
    final_video.write_videofile("output.mp4")

if __name__ == "__main__":
    main()
