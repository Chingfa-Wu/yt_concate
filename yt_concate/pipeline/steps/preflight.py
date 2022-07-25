from .step import Step
from yt_concate.utils import Utils


class Preflight(Step):
    def process(self, data, inputs, utils):
        print('in preflight')
        utils.create_dir()

