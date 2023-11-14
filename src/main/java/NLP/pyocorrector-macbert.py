from pycorrector.macbert.macbert_corrector import MacBertCorrector


def check(content):
    USER_DATA_DIR = os.path.expanduser('~/.pycorrector/datasets/')
    macbert_model_dir = os.path.join(USER_DATA_DIR, 'macbert_models/macbert4csc-base-chinese')

    ar = "macbert_models/macbert4csc-base-chinese"
    macbert = MacBertCorrector(ar)
    nlp = macbert.macbert_correct
    print(nlp(content))

if __name__ == '__main__':
    msg = '阿坝阿坝'
    check(msg)