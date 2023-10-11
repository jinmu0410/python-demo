import pycorrector

def correct(content):
    corrected_sent, detail = pycorrector.correct(content)
    print(corrected_sent, detail)

if __name__ == '__main__':
    content = '为什么喜欢打加'
    correct(content)