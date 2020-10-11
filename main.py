import time

from Youtube import Youtube

if __name__ == "__main__":
    while True:
        youtube = Youtube()
        videoId = '9GinJ8oT_sg'
        cat_id = "22"
        text = youtube.get_latest_comment(videoId)
        if text is not None:
            youtube.update_name(text, cat_id, videoId)
        else:
            print("Re-Trying Out in 60s")
            time.sleep(60)
