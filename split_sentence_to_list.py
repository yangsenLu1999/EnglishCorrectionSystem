import re
def splited_sentence(sentence):
    # 利用正则表达式匹配文本中的单词和标点符号
    splited_sentence = re.findall(r'\b\w+\b|[^\w\s]', sentence)
    return splited_sentence

if __name__ == '__main__':
    sentence = "However, learning to understand and to share the value system of a society cannot be achieved only in home. "
    splited_sentence = splited_sentence(sentence)
    print(splited_sentence)