import unicodedata
import praw
import urllib.request
from urllib.error import HTTPError
from moviepy.editor import *
import shutil
import os
import re
from datetime import datetime

temp ="./temp/"

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


def getSubredditCompilation(reddit, subreddit_name, limit):
    final_clip = []
    subredditW = reddit.subreddit(subreddit_name)
    retreival_param = subredditW.top("week",limit=5)
    for submission in retreival_param:
        video_url = submission.media["reddit_video"]["fallback_url"]
        audio_url = video_url.split("DASH_")[0] + "audio"
        audio_file = temp + escaped_title+".mp3"
        video_file = temp + escaped_title+".mp4"

        escaped_title = get_valid_filename(submission.title)
        urllib.request.urlretrieve(video_url, video_file)
        # Handling case of no audio as well
        try:
            urllib.request.urlretrieve(audio_url, audio_file)
            videoClip = VideoFileClip(video_file)
            videoClip = videoClip.set_audio(AudioFileClip(audio_file))
            final_clip.append(videoClip)
        except  HTTPError as ex:
            videoClip = VideoFileClip(video_file)
            final_clip.append(videoClip)
    final_video = concatenate_videoclips(final_clip,method='compose')
    current_timestamp = datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p")
    final_video.write_videofile(subreddit_name+current_timestamp+".mp4")

def main():
    shutil.rmtree(temp, ignore_errors=True)
    os.makedirs(temp)
    reddit = praw.Reddit(client_id=os.environ["client_id"],
                        client_secret=os.environ["client_secret"],
                        user_agent=os.environ["user_agent"])
    getSubredditCompilation(reddit,"watchpeopledieinside",10)

if __name__ == "__main__":
    main()
