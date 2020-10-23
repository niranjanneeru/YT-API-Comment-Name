import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class Youtube:
    title = ''

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
                flow = InstalledAppFlow.from_client_secrets_file('secrets/sec.json',
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

    def get_latest_comment(self, video_id) -> str:
        print("Fetching Comments...")
        request = self.youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
        )

        try:
            response = request.execute()
            results = response['items']
            flag = 0
            pin = 1
            while True:

                if os.path.exists('secrets/comment.pickle'):
                    print('Loading Comment From File...')
                    with open('secrets/comment.pickle', 'rb') as comment:
                        self.title = pickle.load(comment)

                if not flag and self.title == results[1]['snippet']['topLevelComment']['snippet']['textDisplay']:
                    print("No New Comments...")
                    break
                elif not flag:
                    self.title = results[1]['snippet']['topLevelComment']['snippet']['textDisplay']
                    with open('secrets/comment.pickle', 'wb') as file:
                        print("Saving Comment...")
                        pickle.dump(self.title, file)
                for result in results:
                    if pin:
                        pin = 0
                        continue
                    text = result['snippet']['topLevelComment']['snippet']['textDisplay']
                    if text.startswith('New Title:-'):
                        return text[len("New Title:-"):]
                if 'nextPageToken' in response:
                    request = self.youtube.commentThreads().list(
                        part='snippet',
                        videoId=video_id,
                        pageToken=response['nextPageToken']
                    )
                    flag = 1
                    response = request.execute()
                    results = response['items']
                else:
                    break
        except Exception as e:
            print(e)
            return None

    def update_name(self, text: str, cat_no: str, video_id: str):
        print("Setting Name to " + text)
        request = self.youtube.videos().update(
            part="snippet",
            body={
                "id": video_id,
                "snippet": {
                    "title": "Realtime Title: " + text,
                    "categoryId": cat_no,
                    "description": """Instruction: You just need to comment on it, See the title changes within a span of 60s

Implementation Video:- https://youtu.be/Ep8owfBeOyk

Resources:- https://github.com/niranjanneeru/YT-API-Comment-Name

The Project Walkthrough takes you to the vast possibility of Google API, especially Youtube API, the whole process of Authenticating, Updating, Fetching Comments, and Views. Google OAuth Library is explained for Authentication and making API calls 


For Deployment:- https://youtu.be/Ep8owfBeOyk
Python Anywhere  & Digital Ocean

Playlist: https://www.youtube.com/playlist?list=PLMRsauON0vW2T2LIguI23oMeQPn7DPGIn


🌎 Website https://codersofgreyhavens
⭐ Discord: https://discord.gg/6eBZxF

📂 GitHub: https://github.com/niranjanneeru


⚡ Please leave a LIKE and SUBSCRIBE for more content! ⚡

Tags:
- Coders of grey havens
- Python Tutorials
- API
- Youtube API
- Google OAuth

#python #api #ytapi #oauth #developerconsole #pycharm #vscode #pythonanywhere""",
                    "tags": [
                        'Coders of grey havens', 'Python Tutorials', 'api', 'ytapi', 'oauth', 'developerconsole',
                        'pycharm', 'vscode',
                        'pythonanywhere', 'python', 'Youtube API', 'Google OAuth'
                    ],
                }
            }
        )
        try:
            request.execute()
        except Exception as e:
            print(e)

    def getViews(self, video_id):
        request = self.youtube.videos().list(
            part="statistics",
            id=video_id
        )
        try:
            views = request.execute()['items'][0]['statistics']['viewCount']
            print("No of views:- " + str(views))
        except Exception as e:
            print(e)
