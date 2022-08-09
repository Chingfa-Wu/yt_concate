from threading import Thread
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
        for yt in yt_set:
            url = yt.url
            if cnt > inputs['limit']:
                logger.info('up to limit')
                break

            if inputs['fast'] and utils.video_file_exists(yt):
                logger.info(f'found existing video for {url}, skipping')
                continue

            logger.info(f'downloading {url}')
            threads.append(Thread(target=self.dl_video, args=(yt,)))

            cnt += 1

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        end = time()
        return data

    @staticmethod
    def dl_video(yt):
        YouTube(yt.url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id + '.mp4')
