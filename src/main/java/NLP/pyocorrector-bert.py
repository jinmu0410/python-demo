from transformers import pipeline

model_id = 'damo/nlp_bart_text-error-correction_chinese'
pipeline = pipeline('test-mask', model=model_id)

print(pipeline('今天新情很好'))