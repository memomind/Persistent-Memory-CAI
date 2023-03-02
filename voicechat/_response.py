import openai
import time

openai.api_key=''

def reply(msg:str):
    def query_openai():
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f'''{msg}
要求：
1.用粵語回答
2.回覆中不要介紹你自己
3.回覆中不要重複我的問題
'''}]
            )
            return completion
        except:
            time.sleep(1)
            query_openai()

    completion = query_openai()
    response = completion['choices'][0]['message']['content'].strip()
    return response

