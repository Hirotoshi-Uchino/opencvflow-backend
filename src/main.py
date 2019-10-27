import json
import sys
import traceback

from log import setup_logger
from pipeline_parser import PipelineParser


def exec_pipeline(img_ndarray, pp):
    result = {'resultList': []}
    existsError = False
    trace = ''
    for p in pp.parse():
        process  = p['process']

        try:
            img_ndarray, base64 = process.do(img_ndarray)
            this_result = {'blockId': p['block_id'], 'base64': base64}
            result['resultList'].append(this_result)

        except:
            existsError = True
            trace = traceback.format_exc()

            break

    logger.info('pipeline end.')
    if existsError:
        resultHeader = {'code': '002'}
        result = {'header': resultHeader}
        result['errorMessage'] = trace
    else:
        resultHeader = {'code': '000'}
        result['header'] = resultHeader

    return result

if __name__ == '__main__':
    args = sys.argv
    pipelineInfoString = args[1]

    logger = setup_logger(__name__, './logs/process.log')

    logger.info('pipeline start.')
    logger.info('pipelineInfoString' + pipelineInfoString)

    pp = PipelineParser(pipelineInfoString)

    img_ndarray = pp.get_image()

    if img_ndarray is None:
        resultHeader = {'code': '001'}
        result = {'header': resultHeader}
        result = {'errorMessage': pp.imageFilePath + ': No such file.'}
    else:
        result = exec_pipeline(img_ndarray, pp)


    print(json.dumps(result))