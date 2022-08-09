from .steps.step import StepException
from yt_concate.utils import Utils

import logging
logger = logging.getLogger()

utils = Utils()


class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def run(self, inputs):
        data = None

        for step in self.steps:
            try:
                data = step.process(data, inputs, utils)
            except StepException as e:
                logger.warning(f'Exception happened: {e}')
                break
