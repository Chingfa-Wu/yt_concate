import time

from threading import Thread
from concurrent.futures import ThreadPoolExecutor

from pytube import YouTube

from .step import Step

import logging
logger = logging.getLogger()

threads = []


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        with ThreadPoolExecutor() as executor:
            for yt in data:
                logger.info(f'downloading caption for {yt.id}')
                if inputs['fast'] and utils.caption_file_exists(yt):
                    logger.info('found exists file')
                    continue
                executor.submit(self.dl_cap(yt, utils,))

        end = time.time()
        logger.info(f'download caption using {end - start}')
        return data

    def dl_cap(self, yt, utils):
        try:
            source = YouTube(yt.url)
            if source.length < 30*60:
                en_caption = source.captions['a.en']
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
                text_file = open(utils.get_caption_filepath(yt.url), "w", encoding='utf-8')
                text_file.write(en_caption_convert_to_srt)
                text_file.close()

                lines = open(utils.get_caption_filepath(yt.url), "r", encoding='utf-8').readlines()
                start_t, end_t, end = self.parse_caption_time(lines[-2])
                if end > source.length:
                    lines[-2] = f'{start_t} --> {end_t}:{source.length / (3600*60)},000'
                    open(utils.get_caption_filepath(yt.url), "w", encoding='utf-8').write(lines)
            else:
                logger.debug(f'this video {yt.id} is too long')
        except (KeyError, AttributeError):
            logger.warning(f'Error when downloading {yt.id}')
        except TypeError:
            pass

    def parse_caption_time(self, caption_time):
        start, end = caption_time.split(' --> ')
        return start, self.parse_time_cut(end), self.parse_time_cnt(end)

    @staticmethod
    def parse_time_cnt(time_str):
        h, m, s = time_str.split(':')
        s, ms = s.split(',')
        return int(h)*3600 + int(m)*60 + int(s) + int(ms) / 1000

    def parse_time_cut(self, time_str):
        h, m, s = time_str.split(':')
        return f'{h}:{m}'
