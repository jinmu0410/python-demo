import json
import numpy as np

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import sys

# 从文本中提取关键字
def key_word_extract(content):
    ner_pipeline = pipeline(Tasks.named_entity_recognition,
                            'damo/nlp_structbert_keyphrase-extraction_base-icassp2023-mug-track4-baseline')

    result = ner_pipeline(content)
    out = result.get('output')
    print(out)
    print(type(out))
    print(json.dumps(out,default=convert_int64))

    # return ner_pipeline(content)


def convert_int64(o):
    if isinstance(o, np.int64):
        return int(o)
    raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')

if __name__ == '__main__':
    #key_word_extract("杭州是个好地方")
    key_word_extract("哎大家好啊欢迎大家准时来参加我们的会议，今天我们会议的主题呢是如何提升我们这个洗发水儿的品牌影响力啊。我们现在是主要的产品是这个霸王防脱洗发水儿，现在请大家发表自己的意见啊欢迎大家努力的发表，请先从这位男士开始")