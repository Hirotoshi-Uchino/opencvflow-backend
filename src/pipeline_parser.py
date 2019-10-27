import json
import os
import cv2
from process import GrayScale, Binarization, Filter, Gradient


class PipelineParser():

    process_map = {
        1: GrayScale,
        2: Binarization,
        3: Filter,
        4: Gradient,
    }

    def __init__(self, pipelineInfoString):
        self.pipelineInfoString = pipelineInfoString
        self.pipelineInfo  = json.loads(pipelineInfoString)
        self.imageFilePath = self.pipelineInfo.get('imageFilePath')

    def get_image(self):
        if self.imageFilePath is None:
            return False

        self.img_ndarray = cv2.imread(self.imageFilePath)
        return self.img_ndarray

    def parse(self):

        p, ext = os.path.splitext(self.imageFilePath)

        process_instances = [] # {blockId: process_instance} が入る
        for process in self.pipelineInfo.get('pipeline'):
            process_id = process['processId']
            block_id   = process['blockId']
            parameters = process['parameters']

            detail_process = ''
            if 'detailProcess' in parameters:
                detail_process = parameters['detailProcess']

            detail_parameters = {}
            if 'detailParameters' in parameters:
                detail_parameters = parameters['detailParameters']

            process_instance = self.process_map[process_id](ext, detail_process, detail_parameters)
            process_instances.append({'block_id': block_id, 'process': process_instance})

        return process_instances