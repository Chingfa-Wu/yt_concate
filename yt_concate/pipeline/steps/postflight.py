from .step import Step

import logging
logger = logging.getLogger()


class Postflight(Step):
    def process(self, data, inputs, utils):
        logger.info('in postflight')
        if inputs['clean_up']:
            utils.delete()
            logger.info('done to delete caption and video')
