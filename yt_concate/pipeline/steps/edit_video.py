from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips
from .step import Step

import logging
logger = logging.getLogger()


class EditVideo(Step):
    def process(self, data, inputs, utils):
        clips = []
        for found in data:

            start, end = self.parse_caption_time(found.time)
            logger.debug(f'start = {start}, end = {end}, cap = {found.caption}')
            video = VideoFileClip(found.yt.video_filepath).subclip(start, end)

            clips.append(video)

            if len(clips) >= inputs['limit']:
                break

        final_clip = concatenate_videoclips(clips)

        output_filepath = utils.get_output_filepath(inputs['channel_id'], inputs['search_word'])

        try:
            final_clip.write_videofile(output_filepath,
                                       codec='libx264',
                                       audio_codec='aac',
                                       temp_audiofile='temp-audio.m4a',
                                       remove_temp=True)
            final_clip.close()
        except OSError:
            pass
        for ele in clips:
            ele.reader.close()
            ele.audio.reader.close_proc()

    def parse_caption_time(self, caption_time):
        start, end = caption_time.split(' --> ')
        return self.parse_time_str(start), self.parse_time_str(end)

    def parse_time_str(self, time_str):
        h, m, s = time_str.split(':')
        s, ms = s.split(',')
        return int(h), int(m), int(s) + int(ms) / 1000
