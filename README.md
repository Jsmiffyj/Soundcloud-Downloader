# Soundcloud-Downloader
Python script w/ GUI to download non GO+ songs from Soundcloud


![image](https://github.com/user-attachments/assets/0c960a0b-eaa0-452c-b214-900c44f30a8e)






Requirements:
yt-dlp (for downloading) - https://github.com/yt-dlp/yt-dlp
ffmpeg (for converting file type) - https://www.ffmpeg.org
python

-------------------------------------------------------------------



Created using own skills and a bit of ChatGPT, this script is used to download songs from Soundcloud in the highest quality.
If you are a Soundcloud GO+ member make sure to to enable "High Streaming Quality" in the Soundcloud settings. Also you can use your OAuth token to download higher quality audio as well as GO+ only songs.

![image](https://github.com/user-attachments/assets/a54fc6e5-59b6-4b78-a2ef-6e578b71a91e)

Below is a guide on how to find your OAuth if you are a Soundcloud GO+ member.

1. Open Soundcloud and log into your premium account
2. Open up developer tools in the browser (Ctrl+Shift+i)
3. Go to the Network tab
4. Filter "auth"
5. Find your session packet and checkl the payload for the session access token, that is your OAuth token
![image](https://github.com/user-attachments/assets/fd75511a-9445-4632-8c33-cf77ded93ba6)
