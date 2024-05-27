import whisper
from pydub import AudioSegment
from pydub.silence import split_on_silence
from transformers.models import openai
import os

model = whisper.load_model("large")

# 使用Whisper本地进行音频转录
def transcribe_audio_whisper(path):
    result = model.transcribe(path)
    text = result['text']
    return text

def translate_text_to_chinese(text):
    translation = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"将以下英文文本翻译成中文: '{text}'",
        max_tokens=1000,
    )

    translated_text = translation.choices[0].text.strip()
    return translated_text

# 将音频文件根据静音部分分割成块，并使用Whisper API进行语音识别的函数
def get_large_audio_transcription_on_silence_whisper(path, export_chunk_len):
    sound = AudioSegment.from_file(path)
    chunks = split_on_silence(sound, min_silence_len=500, silence_thresh=sound.dBFS-14, keep_silence=500)

    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    # 现在重新组合这些块，使得每个部分至少有export_chunk_len长。
    output_chunks = [chunks[0]]
    for chunk in chunks[1:]:
        if len(output_chunks[-1]) < export_chunk_len:
            output_chunks[-1] += chunk
        else:
            # 如果最后一个输出块的长度超过目标长度， 我们可以开始一个新的块
            output_chunks.append(chunk)

    whole_text = ""
    for i, audio_chunk in enumerate(output_chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.mp3")
        audio_chunk.export(chunk_filename, format="mp3")

        try:
            text = transcribe_audio_whisper(chunk_filename)
        except Exception as e:
            print("Error:", str(e))
        else:
            text = f"{text.capitalize()}. "
            print(chunk_filename, ":", text)
            whole_text += text

    return whole_text


if __name__ == '__main__':
    path="/Users/jinmu/Downloads/ffmpeg/output_audio.mp3"
    export_chunk_len = 90 * 1000

    audio_text = get_large_audio_transcription_on_silence_whisper(path, export_chunk_len)
    print("\nAudio Full text:", audio_text)

    chinese_audio_translation = translate_text_to_chinese(audio_text)
    print("\nAudio Translate text:", chinese_audio_translation)

