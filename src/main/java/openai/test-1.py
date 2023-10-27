import openai

msg = input()

openai.api_key = "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"

response = openai.Completion.create(
    engine ="text-davinci-003",
    prompt = msg,
    max_tokens = 1024,
    #conversation_id = convId
    #temperature = 0.2,
    #n = 1
)

ans = str(response.choices[0].text)[str(response.choices[0].text).find('\n')+1:]

print(ans)
