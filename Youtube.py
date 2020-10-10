import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class Youtube:
    def __init__(self):
        credentials = None
        if os.path.exists('token.pickle'):
            print('Loading Credentials From File...')
            with open('token.pickle', 'rb') as token:
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
                flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message='')
                credentials = flow.credentials

            with open('token.pickle', 'wb') as file:
                print("Saving...")
                pickle.dump(credentials, file)

        self.youtube = build('youtube', 'v3', credentials=credentials)

    def get_latest_comment(self, video_id) -> str:
        print("Fetching Comments...")
        request = self.youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
        )

        response = request.execute()

        results = response['items']
        flag = 1
        while flag:
            for result in results:
                text = result['snippet']['topLevelComment']['snippet']['textDisplay']
                if text.startswith('New Title:-'):
                    return text
            if 'nextPageToken' in response:
                request = self.youtube.commentThreads().list(
                    part='snippet',
                    videoId='9GinJ8oT_sg',
                    pageToken=response['nextPageToken']
                )
                response = request.execute()
                results = response['items']
            else:
                break

    def update_name(self, text, cat_no):
        print("Setting Name to " + text)
        request = self.youtube.videos().update(
            part="snippet",
            body={
                "id": "9GinJ8oT_sg",
                "snippet": {
                    "title": text,
                    "categoryId": str(cat_no)
                }
            }
        )
        try:
            request.execute()
        except Exception as e:
            print(e)
