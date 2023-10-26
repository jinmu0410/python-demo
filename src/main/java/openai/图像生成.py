import openai

openai.api_key = "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"

# 生成图像
def work(msg):
    response = openai.Image.create(
        prompt=msg,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    print(image_url)

if __name__ == '__main__':
   msg = 'A fluffy white cat with blue eyes sitting in a basket of flowers, looking up adorably at the camera';
   work(msg)



