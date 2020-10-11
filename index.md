# YT API Comment Name

Script uses Youtube API to access the comment and set it as the title of the video

### Useful Links

[Youtube Tutorial]() <br>
[Developer Console](https://console.developers.google.com/) <br>
[Data API V3 Getting started](https://developers.google.com/youtube/v3/getting-started) <br>
[Google Python Client API Github](https://github.com/googleapis/google-api-python-client) <br>
[Pickle Module Docs](https://docs.python.org/3/library/pickle.html) <br>
[Scopes](https://developers.google.com/identity/protocols/oauth2/scopes#youtube) <br>
[Installed Apps](https://developers.google.com/youtube/v3/live/guides/auth/installed-apps) <br>
[Youtube Data V3 Docs](https://developers.google.com/youtube/v3/docs)

### PythonAnywhere Deployment

Create Virtual Environment

```
python3 -m venv ytenv
source ytenv/bin/activate
```

Installing Requirements

```
pip install -r requirements.txt
```

Running main.py

```
python3 main.py <videoId> <categoryId>
```
videoId in the url
categoryId given below

### OAuth

<img src ="https://github.com/niranjanneeru/YT-API-Comment-Name/blob/master/raw/OAuth.jpeg?raw=true">


### List of Category Id

1 -  Film & Animation<br>
2 - Autos & Vehicles<br>
10 - Music<br>
15 - Pets & Animals<br>
17 - Sports<br>
18 - Short Movies<br>
19 - Travel & Events<br>
20 - Gaming<br>
21 - Video Blogging<br>
22 - People & Blogs<br>
23 - Comedy<br>
24 - Entertainment<br>
25 - News & Politics<br>
26 - Howto & Style<br>
27 - Education<br>
28 - Science & Technology<br>
29 - Nonprofits & Activism<br>
30 - Movies<br>
31 - Anime/Animation<br>
32 - Action/Adventure<br>
33 - Classics<br>
34 - Comedy<br>
35 - Documentary<br>
36 - Drama<br>
37 - Family<br>
38 - Foreign<br>
39 - Horror<br>
40 - Sci-Fi/Fantasy<br>
41 - Thriller<br>
42 - Shorts<br>
43 - Shows<br>
44 - Trailers<br>


## Step 
#### 1
Start a project in developer Console Google
Link in README.md
#### 2
Install Youtube Data API V3
from Libraries 
#### 3
Create OAuth Consent Screen
#### 4
Create OAuth Client ID Credential
#### 5
Download Credentials as JSON Data
Store it as src/sec.json
#### 6
Youtube Class
#### 7
OAuth Image
#### 8
Authenticate Application with OAuth with in __init__
```python
from google_auth_oauthlib.flow import InstalledAppFlow
def __init__(self):
    print('Fetching New Tokens...')
    flow = InstalledAppFlow.from_client_secrets_file('sec.json',
                                                     scopes=[
                                                         'https://www.googleapis.com/auth/youtube.force-ssl',
                                                         'https://www.googleapis.com/auth/youtubepartner',
                                                         'https://www.googleapis.com/auth/youtube'])
    flow.run_local_server(prompt='consent', authorization_prompt_message='')
    credentials = flow.credentials
```
#### 9
Update __init__ method
```python
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
def __init__(self):
    print('Fetching New Tokens...')
    flow = InstalledAppFlow.from_client_secrets_file('sec.json',
                                                     scopes=[
                                                         'https://www.googleapis.com/auth/youtube.force-ssl',
                                                         'https://www.googleapis.com/auth/youtubepartner',
                                                         'https://www.googleapis.com/auth/youtube'])
    flow.run_local_server(prompt='consent', authorization_prompt_message='')
    credentials = flow.credentials
    self.youtube = build('youtube', 'v3', credentials=credentials)
```
#### 10
Get_Latest_Comment() Method
```python
def get_latest_comment(self, video_id):
    print("Fetching Comments...")
    request = self.youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
    )
```
#### 11
Execute and print json
```python
def get_latest_comment(self, video_id):
    print("Fetching Comments...")
    request = self.youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
    )
    response = request.execute()
    print(response)
```
#### 12
Parse Out Comments
```python
results = response['items']
for result in results:
    text = result['snippet']['topLevelComment']['snippet']['textDisplay']
    print(text)
```
#### 13
Update Title <br>
Refer Docs update() Method
```python
request = self.youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": {
                "title": text,
                "categoryId": cat_no
            }
        }
    )
```
Execute
```python
def update_name(self, text: str, cat_no: str, video_id: str):
    print("Setting Name to " + text)
    request = self.youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": {
                "title": text,
                "categoryId": cat_no
            }
        }
    )
    request.execute()
```
#### 14
Catch Exceptions
```python
def update_name(self, text: str, cat_no: str, video_id: str):
    print("Setting Name to " + text)
    request = self.youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": {
                "title": text,
                "categoryId": cat_no
            }
        }
    )
    try:
        request.execute()
    except Exception as e:
        print(e)
```

#### 15
main.py
```python
from src.Youtube import Youtube

if __name__ == "__main__":
    video_id = '<some Link>'
    cat_id = '<catId> : Refer Github'
    youtube = Youtube()
    youtube.get_latest_comment(video_id)
    text = "Hi New Title"
    youtube.update_name(text, cat_id, video_id)
```

#### 16
Refer Command Prompt

#### 17
Authentication Efficiency 

Pickle
```python
import pickle

with open('secrets/token.pickle', 'wb') as file:
    print("Saving Tokens...")
    pickle.dump(credentials, file)
```
```python
import pickle
import os

if os.path.exists('secrets/token.pickle'):
    print('Loading Credentials From File...')
    with open('secrets/token.pickle', 'rb') as token:
        credentials = pickle.load(token)
```

Incorporating ....
```python
import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def __init__(self):
    credentials = None
    if os.path.exists('secrets/token.pickle'):
        print('Loading Credentials From File...')
        with open('secrets/token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file('sec.json',
                                                             scopes=[
                                                                 'https://www.googleapis.com/auth/youtube.force-ssl',
                                                                 'https://www.googleapis.com/auth/youtubepartner',
                                                                 'https://www.googleapis.com/auth/youtube'])
            flow.run_local_server(prompt='consent', authorization_prompt_message='')
            credentials = flow.credentials

        with open('secrets/token.pickle', 'wb') as file:
            print("Saving Tokens...")
            pickle.dump(credentials, file)

    self.youtube = build('youtube', 'v3', credentials=credentials)
```

#### 18
Fetching Comments from nextPageToken
```python
def get_latest_comment(self, video_id) -> str:
    print("Fetching Comments...")
    request = self.youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
    )

    try:
        response = request.execute()
        results = response['items']
        while True:
            for result in results:
                text = result['snippet']['topLevelComment']['snippet']['textDisplay']
                if text.startswith('New Title:-'):
                    return text[len("New Title:-"):]
            if 'nextPageToken' in response:
                request = self.youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    pageToken=response['nextPageToken']
                )
                response = request.execute()
                results = response['items']
            else:
                break
    except Exception as e:
        print(e)
        return None
```

#### 19
No New Comments Message <br>
Declare title variable
```python
if os.path.exists('comment.pickle'):
    print('Loading Comment From File...')
    with open('comment.pickle', 'rb') as comment:
        self.title = pickle.load(comment)

if not flag and self.title == results[0]['snippet']['topLevelComment']['snippet']['textDisplay']:
    print("No New Comments...")
    break
elif not flag:
    self.title = results[0]['snippet']['topLevelComment']['snippet']['textDisplay']
    with open('comment.pickle', 'wb') as file:
        print("Saving Comment...")
        pickle.dump(self.title, file)
```

#### 20
main.py
```python
import sys
import time

from src.Youtube import Youtube

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Specify videoId and Category Id\nRefer :-" +
              "https://github.com/niranjanneeru/YT-API-Comment-Name\npython main.py <videoId> <categoryId>")
    else:
        videoId = sys.argv[1]
        cat_id = sys.argv[2]
        while True:
            youtube = Youtube()
            youtube.getViews(videoId)
            text = youtube.get_latest_comment(videoId)
            if text is not None:
                youtube.update_name(text, cat_id, videoId)
                print("Re-Trying in 30s...")
                time.sleep(30)
            else:
                print("Re-Trying in 60s...")
                time.sleep(60)
```
