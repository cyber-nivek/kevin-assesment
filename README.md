## This is my attempt at tackling the technical assesment. 
### A program that when executed, locates a desired youtube video or channel and transcribes its audio contents to text, through the use of OpenAI's Whisper model.

It is a simple enough Python script, to be executed through terminal or any other desired methods, but it does not require anything in on itself. Once you launch the program, some pop-up windows will appear asking you for information. In order, the information required is:
- Google API Key: Your Google API Key, so the Youtube API can be accessed. Its length and characters are not currently controlled, but they should be.
- Channel name: This can be either a channel name (the name when you open a user's profile on YT, not necesarily what comes after the @ symbol on the url), where several latest videos will be transcripted, or directly a youtube video url following the format "https://www.youtube.com/watch?v=" followed by the video ID.
- Debug mode: Indicated by entering "True". Any other input will be interpreted as false and the flag will be desactivated. Currently it simply adds a full print of the model's log when it is processing the audio file.

That is it regarding user imput, which by the way I am fully aware it could be cleaner. Regardless, the way the program works is by taking a reference to specific youtube content, be it a channel name, or a video url, locating its id and properties through the api, downloading it in audio format (mp3) and feeding it to the Whisper model, which is also download if needed. 

The Whisper model used is the base one; with the medium or large one better results could be achived. However, that would also significantly increase the load in the program, and slow it down significantly. On top of that, my laptom did not seem to be capable of using gpu acceleration for the feed forward (CUDA), so testing has been painfully slow. Despite that, results seem to be generally really good. 

With that out of the way, I wanted to comment how I deviated inevitably from the original task that I was suppposed to perform. Mainly, my focus on channel managment, and the entire omision on the 10 request limit per minute. For the first one, I understood the "you may recieve up to 10 video transcriptions, and you may expect them from the same channel" as "you will be working within a single channel", so I focused on that, and ended up being the main functional mode of the program. I did not want it to go to gaste, so I kept it.By default, It loads and processes the five latest videos (which includes shorts, I have discovered) 

On the other hand, about the request handling, I simply did not see how to properly implement it at the moment. I think I took more than enough to work on this project, and this release is close to overdue. For this reason, and the fact that my PC could not reach this limit anyway (whithout gpu use or multithreading, the second of which I would have implemented as a next step), I decided to focus in what I considered the main functionality.

I wanted to comment also on a bug I found towards the end of development; Certain videos names, to be specific, those contanining special characters such as "|" cannot be handled correctly, and will result in the program failing when trying to feed the audio file to the model. I have tried solving it (one attempt can still be seen on code commented), but could not find a proper way of solving it as of now.

Lastly, and unless I am forgetting something else, here is a list of the library dependencies requiered, alongside the version I used:

- ffmpeg-python (v0.2)
- google-api-core (2.14.0)
- google-api-python-client (v2.109.0)
- openai-whisper (v20231117)
- yt-dlp (v2003.12.5.232702.dev0)

Thank you for reading, and I hope you find my implementation interesting!
