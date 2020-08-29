# Works only on linux since ffmpeg code is not cross platform
import unicodedata
import praw
import urllib.request
from urllib.error import HTTPError
import subprocess
import shutil
import os
import re
import glob
temp ="./temp/"
final ="./final/"
import re
import unidecode

def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

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

def write_to_file():
    os.chdir(final)
    listFiles = glob.glob("*")
    param=""
    for fileobj in listFiles:
        param=param + " -i " + fileobj
    cmd = 'ffmpeg %s \
       -filter_complex "[0:v] [0:a] [1:v] [1:a] [2:v] [2:a] concat=n=3:v=1:a=1 [v] [a]" \
       -map "[v]" -map "[a]" output.mkv' %(param)
    print(cmd)
    subprocess.call(cmd, shell=True)

def handleSubmissionMedia(submission):
    video_url = submission.media["reddit_video"]["fallback_url"]
    audio_url = video_url.split("DASH_")[0] + "audio"
    escaped_title = slugify(submission.title)
    print(submission.title)
    urllib.request.urlretrieve(video_url, temp + escaped_title+".mp4")
    # Handling case of no audio as well
    try:
        urllib.request.urlretrieve(audio_url, temp + escaped_title+".mp3")
        cmd = 'ffmpeg -i %s -i %s -c:v copy -c:a aac -strict experimental %s' % ( temp+escaped_title+".mp4",  temp+escaped_title+".mp3", final+escaped_title+".mp4")
        subprocess.call(cmd, shell=True)
    except  HTTPError as ex:
        os.replace(temp+escaped_title+".mp4", final+escaped_title + ".mp4")
    return final+escaped_title+".mp4"
def main():
    clean_all()
    reddit = praw.Reddit(client_id=os.environ["client_id"],
                        client_secret=os.environ["client_secret"],
                        user_agent=os.environ["user_agent"])
    print(reddit.read_only)
    subredditW = reddit.subreddit("watchpeopledieinside")
    param=""
    for submission in subredditW.top(limit=5):
        param= param +" -i " + handleSubmissionMedia(submission)
    write_to_file()

if __name__ == "__main__":
    write_to_file()
