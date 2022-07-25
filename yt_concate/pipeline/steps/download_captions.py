from pytube import YouTube

from .step import Step
from .step import StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        channel_id = inputs['channel_id']
        black_list = self.read_file(utils.get_video_list_filepath(f'{channel_id}_blacklist'))

        for yt in data:
            print('downloading caption for', yt.id)
            if utils.caption_file_exists(yt):
                print('found exists file')
                continue
            if yt.url in black_list:
                print(f'this video {yt.url} is in black list')
                continue

            try:
                source = YouTube(yt.url)
                en_caption = source.captions['a.en']
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            except AttributeError:
                continue
            except KeyError:
                print('KeyError when downloading caption for', yt.url, 'adding to black list')
                black_list.append(yt.url)
                continue
            print(en_caption_convert_to_srt)

            text_file = open(utils.get_caption_filepath(yt.url), "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()

        self.write_to_file(black_list, utils.get_video_list_filepath(f'{channel_id}_blacklist'))
        return data

    def write_to_file(self, lst, filepath):
        with open(filepath, 'w') as f:
            for url in lst:
                f.write(url + '\n')

    def read_file(self, filepath):
        video_links = []
        with open(filepath, 'r') as f:
            for url in f:
                video_links.append(url.strip())
        return video_links
