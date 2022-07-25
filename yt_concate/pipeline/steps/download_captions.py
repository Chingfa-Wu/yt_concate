from pytube import YouTube

from .step import Step
from .step import StepException

from yt_concate.settings import CAPTIONS_DIR

import time


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        for url in data:
            print('downloading caption for', url)
            if utils.caption_file_exists(url):
                print('found exists file')
                continue
            try:
                source = YouTube(url)
                en_caption = source.captions['a.en']
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            except AttributeError:
                continue
            except KeyError:
                print('KeyError when downloading caption for', url)
                continue
            print(en_caption_convert_to_srt)

            text_file = open(utils.get_caption_filepath(url), "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()
        end = time.time()
        print(f'took {end - start} sec')
