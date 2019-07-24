from moviepy.editor import *
import requests


class VideoService():

    BASE_URL = "http://webapp:8080/static/{}"
    ProcessedFile = "video-processed-{}.mp4"

    @staticmethod
    def process_interval(video_url, interval_time):
        result = []
        name = video_url.rsplit('/', 1)[1]
        r = requests.get(video_url, allow_redirects=True)
        open('static/'+name, 'wb').write(r.content)
        clip = VideoFileClip('static/'+name)
        if clip.duration < interval_time:
            result.append({"video_url": VideoService.BASE_URL.format(name)})
        else:
            no_of_file = int(int(clip.duration) / interval_time) + 1
            for i in range(0, no_of_file):
                new_name = VideoService.ProcessedFile.format(i)
                start = i*interval_time
                end = min((i+1)*interval_time, clip.duration)
                clip.subclip(start, end).write_videofile("static/"+new_name)

                result.append({"video_url" : VideoService.BASE_URL.format(new_name)})

        return {"interval_videos": result}

    @staticmethod
    def process_ranges(video_url, ranges):
        result = []
        name = video_url.rsplit('/', 1)[1]
        r = requests.get(video_url, allow_redirects=True)
        open('static/'+name, 'wb').write(r.content)
        clip = VideoFileClip('static/'+name)
        i = 0
        for part in ranges:
            new_name = VideoService.ProcessedFile.format(i)
            clip.subclip(part.get("start"), part.get("end")).write_videofile("static/"+new_name)
            result.append({"video_url": VideoService.BASE_URL.format(new_name)})
            i += 1

        return {"interval_videos": result}

    @staticmethod
    def process_segments(video_url, no_of_file):
        result = []
        name = video_url.rsplit('/', 1)[1]
        r = requests.get(video_url, allow_redirects=True)
        open('static/' + name, 'wb').write(r.content)
        clip = VideoFileClip('static/' + name)
        interval_time = int( clip.duration) / no_of_file
        for i in range(0, no_of_file):
            new_name = VideoService.ProcessedFile.format(i)
            start = i * interval_time
            end = min((i + 1) * interval_time, clip.duration)
            clip.subclip(start, end).write_videofile("static/" + new_name)
            result.append({"video_url": VideoService.BASE_URL.format(new_name)})

        return {"interval_videos": result}

    @staticmethod
    def combine_video(video_urls, width, height):
        clips = []
        for video in video_urls:
            video_url = video.get('video_url')
            name = video_url.rsplit('/', 1)[1]
            r = requests.get(video_url, allow_redirects=True)
            open('static/' + name, 'wb').write(r.content)
            clip = VideoFileClip('static/' + name)
            clips.append(clip.subclip(video.get("start"), video.get("end")))

        final_clip = concatenate_videoclips(clips)
        name = VideoService.ProcessedFile.format("final")
        final_clip.resize((height,width)).write_videofile("static/" + name)
        result = {"video_url": VideoService.BASE_URL.format(name)}

        return result
