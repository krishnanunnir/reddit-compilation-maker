# Reddit Compilation Maker

## What does it do?

Generate compilation videos of your favourite subreddit. Youtube has now been overrun by compilation videos lifted off from Reddit, which has been lifted of from somewhere else. 

I wanted to make this process a bit simpler. So I made this tool.

Specify a subreddit and get a readymade compilation video as the output. Its functionalities are limited at the time of making the README.md, which I plan to expand soon.

## How to run it?

Create a .env file based on the .ex-env.

```
cp .ex-env .env
```

Generate an app in Reddit from where you can get the values for client_id and client_secret. Fill these values in the .env file. Activate the .env file by running 

```
source .env
```

Now run it with the command

```
python3 movie.py
```

P.S   
I first tried to create the program with ffmpeg run through subprocess in Python but it really didn't make sense after a while, so I ditched it. I thought I should maintain it since it was educational, it is available in the start.py file.

## Future Additions
[ ] Parameter of the video sort for compilation can be changed.  
[ ] Add an option such that user can choose which videos to include.  
[ ] Set a time limit for the video. Makes compilation videos of nearly that length. 
[ ] Better handling size of the output video.  
[ ] Automatically uploads to youtube at regular intervals.  
[ ] Add support for Glyfy, Streamable  

## Limitations known so far

1. Supports only reddit hosted videos  
