## What does it do?

On giving the input for the subreddit, limit and sort, the python script will generate a video that is a compilation based on the inputs provided for reddit hosted videos.

Sample video
<center>
<iframe width="560" height="315" src="https://www.youtube.com/embed/Hw2mE2FSPgI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</center>

## Motivation and How I built it?

I was watching one of those Youtube videos which are compilations of videos from sub like r/watchpeopledieinside. I thought this process can be automated pretty easily and could be fun.

I started the project and lost motivation for a month, but two days ago, I thought I should finish it up. I started working on the project using the PRAW package for handling Reddit API.

One of the issues I faced was handling videos was Reddit hosts its video and audio separately. So the step involved in handling Reddit posts was to check if a media associated with a post is, in fact, a video. Once confirmed we have to check whether the video has audio, in case we have to merge them together or if it has no audio we can simply add the video.

I thought I could do the video manipulation with FFmpeg run using the subprocess module, but as I went further and further with this I realized it is way too complicated and the learning curve way too steep for this small project. So I started looking for alternatives and found moviepy. I was able to merge video and audio and also all the videos together with moviepy with relative ease.

An issue I kept running into was absence of audio in a video that clearly had audio on Reddit, after trying to debug for few hours, I found Reddit has moved video audio to a new domain for recent uploads, so I was looking at the wrong address for audio. After resolving this, the project was done and I had built it nearly to what I had in mind. There are a lot of issues. I want to add support for gfycat and other streaming services as well[Issue up for grabs].