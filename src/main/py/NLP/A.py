from pycorrector.macbert.macbert_corrector import MacBertCorrector
import sys

def check(content,modelPath):
    if modelPath is None:
        modelPath =  "shibing624/macbert4csc-base-chinese"

    print('1111===' + modelPath)
    nlp = MacBertCorrector(modelPath).macbert_correct
    print("macbert_corrector文本纠错结果=" + nlp(content)[0])

if __name__ == '__main__':
    check("你以天天的在干嘛", '/Users/jinmu/Downloads/self/pycorrector/pycorrector/macbert/output/macbert4csc')