# Chinese-to-English

# 温馨提示: 使用pipeline推理及在线体验功能的时候，尽量输入单句文本，如果是多句长文本建议人工分句，否则可能出现漏译或未译等情况！！！

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

input_sequence = '声明补充说，沃伦的同事都深感震惊，并且希望他能够投案自首。'

pipeline_ins = pipeline(task=Tasks.translation, model="damo/nlp_csanmt_translation_zh2en")
outputs = pipeline_ins(input=input_sequence)

print(outputs['translation'])