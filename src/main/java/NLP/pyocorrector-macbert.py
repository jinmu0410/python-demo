from pycorrector.macbert.macbert_corrector import MacBertCorrector

def check(content):
    nlp = MacBertCorrector("shibing624/macbert4csc-base-chinese").macbert_correct
    print(nlp(content))

if __name__ == '__main__':
  check('以天天的都在做啥')