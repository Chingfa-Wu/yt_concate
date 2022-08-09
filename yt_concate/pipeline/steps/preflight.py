from .step import Step
from yt_concate.utils import Utils

import logging
logger = logging.getLogger()


class Preflight(Step):
    def process(self, data, inputs, utils):

        logger.info('in preflight')
        utils.create_dir()
