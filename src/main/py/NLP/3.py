import torch
from seamless_communication.models.inference import Translator

translator = Translator("seamlessM4T_large", vocoder_name_or_card="vocoder_36langs", device=torch.device("cuda:0"),
                        dtype=torch.float32)

src_lang = "tgl"

tgt_lang = "eng"

input_text = "Salamat sa MetaAI at naglabas sila SeamlessM4T model para gamitin ng mga tao!"

translated_text, wav, sr = translator.predict(input_text, "t2st", tgt_lang=tgt_lang, src_lang=src_lang)

print(translated_text)

src_lang = "cmn"

tgt_lang = "eng"

input_text = "我想购买奶库牛奶"

translated_text, wav, sr = translator.predict(input_text, "t2st", tgt_lang=tgt_lang, src_lang=src_lang)

print(translated_text)

