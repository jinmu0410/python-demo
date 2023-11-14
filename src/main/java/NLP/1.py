from pycorrector.macbert.macbert_corrector import MacBertCorrector

nlp = MacBertCorrector("shibing624/macbert4csc-base-chinese").correct
result = nlp("这仨公司放大舒服")
print(result)
if result['target'] is None:
    print('1' + result['source'])
else:
   print('2' + result['target'])
