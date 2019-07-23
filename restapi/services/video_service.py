from moviepy.editor import *
import requests

class VideoService():

    BASE_URL = "http://localhost:8080/static/{}"
    ProcessedFile = "video-processed-{}.mp4"

    @staticmethod
    def process_interval(video_url, interval_time):
        result = []
        name = video_url.rsplit('/', 1)[1]
        r = requests.get(video_url, allow_redirects=True)
        open('static/'+name, 'wb').write(r.content)
        clip = VideoFileClip('static/'+name)
        if clip.duration < interval_time :
            result.append({"video_url" : VideoService.BASE_URL.format(name)})
        else:
            no_of_file = int(clip.duration) / interval_time + 1
            for i in range(0, no_of_file):
                new_name = VideoService.ProcessedFile.format(i)
                clip.write_videofile("static/"+ new_name)
                result.append({"video_url" : VideoService.BASE_URL.format(new_name)})

        return {"interval_videos": result}