import sys
import time

from Youtube import Youtube

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Specify videoId and Category Id\nRefer :-" +
              "https://github.com/niranjanneeru/YT-API-Comment-Name\npython main.py <videoId> <categoryId>")
    else:
        videoId = sys.argv[0]
        cat_id = sys.argv[1]
        while True:
            youtube = Youtube()
            text = youtube.get_latest_comment(videoId)
            if text is not None:
                youtube.update_name(text, cat_id, videoId)
                print("Re-Trying in 30s...")
                time.sleep(30)
            else:
                print("Re-Trying in 60s...")
                time.sleep(60)
