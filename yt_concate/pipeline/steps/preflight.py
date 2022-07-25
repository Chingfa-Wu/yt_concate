from .step import Step


class Preflight(Step):
    def process(self, data, inputs, utils):
        print('in preflight')
        utils.create_dir()
