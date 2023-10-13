import whisper

model = whisper.load_model('large')
result = model.transcribe(audio='/Users/jinmu/Downloads/111.mp3', language='zh')
print(result["text"])