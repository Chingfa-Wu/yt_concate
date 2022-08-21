from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from time import time

from pytube import YouTube
from yt_concate.settings import VIDEOS_DIR

from .step import Step

import logging
logger = logging.getLogger()

threads = []


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        yt_set = set([found.yt for found in data])
        logger.info(f"video to download = {len(yt_set)}")
        cnt = 0

        start = time()
        with ThreadPoolExecutor() as executor:
            for yt in yt_set:
                url = yt.url
                if cnt > inputs['limit']:
                    logger.info('up to limit')
                    break

                if inputs['fast'] and utils.video_file_exists(yt):
                    logger.info(f'found existing video for {url}, skipping')
                    continue

                logger.info(f'downloading {url}')
                executor.submit(self.dl_video(yt, ))

                cnt += 1

        end = time()
        logger.info(f'download video using {end-start}')
        return data

    @staticmethod
    def dl_video(yt):
        YouTube(yt.url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id + '.mp4')
