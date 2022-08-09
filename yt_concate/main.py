import getopt
import sys
import logging
import time

from yt_concate.pipeline.steps.preflight import Preflight
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.download_captions import DownloadCaptions
from yt_concate.pipeline.steps.read_caption import ReadCaption
from yt_concate.pipeline.steps.search import Search
from yt_concate.pipeline.steps.download_videos import DownloadVideos
from yt_concate.pipeline.steps.edit_video import EditVideo
from yt_concate.pipeline.steps.postflight import Postflight
from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.settings import OUTPUTS_DIR

# CHANNEL_ID = "UCotXwY6s8pWmuWd_snKYjhg"

short_opts = 'hc:w:l:'
long_opts = 'help cleanup fast channel= word= limit= level='.split()


def print_usage():
    print('python3 main.py ARGUMENT')
    print('NECESSARY:')
    print('{:>6} {:<15}{}'.format('-c', '--channel', 'Channel id of the Youtube channel to download'))
    print('{:>6} {:<15}{}'.format('-w', '--word', 'the word that you want to search on Youtube channel'))
    print('OPTIONS:')
    print('{:>6} {:<15}{}'.format('-l', '--limit', 'download video limit(default is 30)'))
    print('{:>6} {:<15}{}'.format('', '--cleanup', 'Remove caption and video after finish'))
    print('{:>6} {:<15}{}'.format('', '--fast', 'if caption or video is exist ,it won\'t download'))
    print('{:>6} {:<15}{}'.format('', '--level', 'which logging level will print on terminal(default is warning)'))
    print('{:>6} {:<15}{}'.format('', '', 'please input debug or info'))


def config_log(inputs):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(message)s')

    file_handler = logging.FileHandler(f"{OUTPUTS_DIR}/{inputs['channel_id']}-{inputs['search_word']}.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(inputs['level'])
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def main(argv):
    inputs = {
        'channel_id': 'UCotXwY6s8pWmuWd_snKYjhg',
        'search_word': 'you',
        'limit': 30,
        'clean_up': True,
        'fast': True,
        'level': logging.WARNING
    }

    try:
        opts, args = getopt.getopt(argv, short_opts, long_opts)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == ('-h', 'help'):
            print_usage()
            sys.exit(0)
        elif opt in ('-c', '--channel'):
            inputs['channel_id'] = arg
        elif opt in ('-w', '--word'):
            inputs['search_word'] = arg
        elif opt in ('-l', '--limit'):
            inputs['limit'] = arg
        elif opt == '--clean_up':
            inputs['clean_up'] = True
        elif opt == '--fast':
            inputs['fast'] = True
        elif opt == '--level':
            if arg == 'debug':
                inputs['level'] = logging.DEBUG
            elif arg == 'info':
                inputs['level'] = logging.INFO

    if not inputs['channel_id'] or not inputs['search_word']:
        print_usage()
        sys.exit(2)

    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaptions(),
        ReadCaption(),
        Search(),
        DownloadVideos(),
        EditVideo(),
        Postflight(),
    ]

    config_log(inputs)
    p = Pipeline(steps)
    p.run(inputs)


if __name__ == "__main__":
    main(sys.argv)


