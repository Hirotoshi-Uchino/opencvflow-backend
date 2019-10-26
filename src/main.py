import json
import sys
import traceback

from pipeline_parser import PipelineParser

args = sys.argv
pipelineInfoString = args[1]

resultHeader = {'code': '000'}
pp = PipelineParser(pipelineInfoString)

img_ndarray = pp.get_image()

result = {'resultList': []}
for p in pp.parse():
    process  = p['process']

    try:
        img_ndarray, base64 = process.do(img_ndarray)
        this_result = {'blockId': p['block_id'], 'base64': base64}
        result['resultList'].append(this_result)

    except:
        print(traceback.format_exc())

print(json.dumps(result))