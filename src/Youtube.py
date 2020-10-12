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
            while True:
                if os.path.exists('secrets/comment.pickle'):
                    print('Loading Comment From File...')
                    with open('secrets/comment.pickle', 'rb') as comment:
                        self.title = pickle.load(comment)

                if not flag and self.title == results[0]['snippet']['topLevelComment']['snippet']['textDisplay']:
                    print("No New Comments...")
                    break
                elif not flag:
                    self.title = results[0]['snippet']['topLevelComment']['snippet']['textDisplay']
                    with open('secrets/comment.pickle', 'wb') as file:
                        print("Saving Comment...")
                        pickle.dump(self.title, file)
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
                    "title": text,
                    "categoryId": cat_no
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
            print("No of views:- "+str(views))
        except Exception as e:
            print(e)
