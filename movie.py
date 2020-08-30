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
sort_dict = {
    "1" : "week",
    "2" : "year",
    "3" : "month",
    "4" : "all",
}
# Copied shamelessly from django
def getValidFilename(s):
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


def getSubredditCompilation(reddit, subreddit_name, limit_no,since):
    final_clip = []
    subredditW = reddit.subreddit(subreddit_name)
    retreival_param = subredditW.top(since,limit=limit_no)
    for submission in retreival_param:
        if submission.is_video:
            video_url = submission.media["reddit_video"]["fallback_url"]
            audio_url = video_url.split("DASH_")[0] + "audio"
            audio_url_alternatvie = video_url.split("DASH_")[0] + "DASH_audio.mp4"
            escaped_title = getValidFilename(submission.title)
            audio_file = temp + escaped_title+".mp3"
            audio_file_alternative = temp + escaped_title+"_audio.mp4"
            video_file = temp + escaped_title+".mp4"
            print(submission.title)
            print(video_url)
            urllib.request.urlretrieve(video_url, video_file)
            # Handling case of no audio as well
            video_clip = VideoFileClip(video_file)
            try:
                print(audio_url)
                urllib.request.urlretrieve(audio_url, audio_file)
                video_clip = video_clip.set_audio(AudioFileClip(audio_file))
            except  HTTPError as ex:
                try:
                    print(audio_url_alternatvie)
                    urllib.request.urlretrieve(audio_url_alternatvie, audio_file_alternative)
                    video_clip = video_clip.set_audio(AudioFileClip(audio_file_alternative))
                except Exception as ex:
                    print(ex)
            final_clip.append(video_clip)
    final_video = concatenate_videoclips(final_clip,method='compose')
    current_timestamp = datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p")
    final_video.write_videofile(subreddit_name+current_timestamp+".mp4")

def getUserInput(reddit):
    subreddit_name = input("Subreddit Name [default: watchpeopledieinside] : ") or "watchpeopledieinside"
    no_of_videos_included = input("Number of posts to be included in the compilation [default: 5] : ") or "5"
    no_of_videos_included = int(no_of_videos_included)
    sort_val = input("sort [1. day 2. week 3. month 4. all] [default: 4] : ") or "4"
    getSubredditCompilation(reddit,subreddit_name,no_of_videos_included,sort_dict[sort_val])

def main():
    shutil.rmtree(temp, ignore_errors=True)
    os.makedirs(temp)
    reddit = praw.Reddit(client_id=os.environ["client_id"],
                        client_secret=os.environ["client_secret"],
                        user_agent=os.environ["user_agent"])
    getUserInput(reddit)

if __name__ == "__main__":
    main()
