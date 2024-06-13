from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.models.nlp import T5ForConditionalGeneration
from modelscope.preprocessors import TextGenerationT5Preprocessor


model = T5ForConditionalGeneration.from_pretrained('ClueAI/ChatYuan-large', revision='v1.0.0')
preprocessor = TextGenerationT5Preprocessor(model.model_dir)
pipeline_t2t = pipeline(task=Tasks.text2text_generation, model=model, preprocessor=preprocessor)

def preprocess(text):
    text = text.replace("\n", "\\n").replace("\t", "\\t")
    return text

def postprocess(text):
    return text.replace("\\n", "\n").replace("\\t", "\t")

def answer(text, sample=True, top_p=1, temperature=0.7):
    '''sample：是否抽样。生成任务，可以设置为True;
    top_p：0-1之间，生成的内容越多样'''
    text = preprocess(text)

    if not sample:
        out_text = pipeline_t2t(text, return_dict_in_generate=True, output_scores=False, max_new_tokens=512, num_beams=1, length_penalty=0.6)
    else:
        out_text = pipeline_t2t(text, return_dict_in_generate=True, output_scores=False, max_new_tokens=512, do_sample=True, top_p=top_p, temperature=temperature, no_repeat_ngram_size=3)

    return postprocess(out_text["text"])


if __name__ == '__main__':
    input_text0 = "帮我写一个请假条，我因为新冠不舒服，需要请假3天，请领导批准"
    print(answer(input_text0))

