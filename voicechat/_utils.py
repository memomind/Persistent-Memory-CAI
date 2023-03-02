import textwrap as tw

def softwrap(text:str,width:int):
    return '\n\n'.join(tw.wrap(text,width, break_on_hyphens=False,break_long_words=False,drop_whitespace=False,fix_sentence_endings=False,expand_tabs=False))


if __name__ == '__main__':
    print(softwrap('''textwrap.wrap("""text = "This is a sample text to demonstrate the line wrapping feature in Python."
words = text.split()  # 把文本按空格分割成单词列表
result = ""  # 用来存储最终结果的字符串
count = 0  # 用来计数已经添加到当前行的单词数量

for word in words:
    if count == 5:  # 当前行已经有5个单词，需要换行
        result += "\n"
        count = 0  # 重置计数器
    result += word + " "
    count += 1

print(result)""",width=300)''',width=30))