#状语
# 补语
# 1.目前不对补语和状语进行区分，补语判断放入状语判断内进行
# 2.对两种特殊情况标记为补语
# (1)“（）”中的成分，作为补语
# (2)“：”后的成分，作为补语
#----------------------------------
#前缀状语：Prefix_Adverbial  后缀状语：Suffix_Adverbial
#----------------------------------
import mydb
import split_sentence_to_list
import parenthetical_phrase
Comma_Index_List=[]
def get_prefix_adverbial_of_the_sentence(splited_sentence:list)->list:
    splited_sentence=splited_sentence
    Comma_Index_List = []
    Prefix_Adverbial_List = []
    #(1)先把句子中所有的逗号找出来并存在列表Comma_Index_List里
    for i in range(len(splited_sentence)):
        #当前字符是英语中的逗号
        if splited_sentence[i]=="，":
            Comma_Index_List.append(i)
        else:
            continue
    for comma_index in Comma_Index_List:
        child_sentence=splited_sentence[:comma_index]
        #(1)前缀状语是单个副词
        if len(child_sentence)==1 and mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(child_sentence[0]):
            Prefix_Adverbial_List.append(child_sentence)
            splited_sentence=splited_sentence[comma_index+1:]

        #(2)前缀状语是To+be 开头的不定式非谓语
        elif child_sentence[0] in ['to', 'To'] and child_sentence[1] == 'be':
            Prefix_Adverbial_List.append(child_sentence)
            splited_sentence = splited_sentence[comma_index + 1:]

        #(3)前缀状语是To+单性动词原型或多性动词原型 为首单词的不定式非谓语
        elif child_sentence[0] in ['to', 'To'] and ( mydb.id_apple_verbpluspos_vori_vsimple(child_sentence[1])>=0 or mydb.id_apple_verbpluspos_double_vori_vcomplex(child_sentence[1])>=0 ):
            Prefix_Adverbial_List.append(child_sentence)
            splited_sentence = splited_sentence[comma_index + 1:]

        #(4)前缀状语是单性动词的现在分词或多性动词的现在分词为首单词的不定式谓语
        elif mydb.id_apple_verbpluspos_vbg_vsimple(child_sentence[0])>=0 or mydb.id_apple_verbpluspos_double_vbg_vcomplex(child_sentence[0])>=0:
            Prefix_Adverbial_List.append(child_sentence)
            splited_sentence = splited_sentence[comma_index + 1:]

        #(5)前缀状语是介词为首单词的 介词结构
        elif mydb.id_apple_prep(child_sentence[0])>=0:
            Prefix_Adverbial_List.append(child_sentence)
            splited_sentence = splited_sentence[comma_index + 1:]

        #(6)前缀状语是 时间状语从句['as','after,'before,'once','since',till,'until','when','whenever','while','as long as','as soon as','now that']
        elif child_sentence[0] in ['as','after','before','once','since','till','until','when','whenever','while','as long as','as soon as','now that']:
            Prefix_Adverbial_List.append(child_sentence)
            splited_sentence = splited_sentence[comma_index + 1:]

        #(7)前缀状语是 地点状语从句['where','wherever','anywhere','everywhere']
        elif child_sentence[0] in ['where','wherever','anywhere','everywhere']:
            Prefix_Adverbial_List.append(child_sentence)
            splited_sentence = splited_sentence[comma_index + 1:]

        # (8)前缀状语是 原因状语从句 ['because','as','since']
        elif child_sentence[0] in ['because','as','since']:
            Prefix_Adverbial_List.append(child_sentence)
            splited_sentence = splited_sentence[comma_index + 1:]

        # (9)前缀状语是 条件状语从句['if','whether','unless','supposing','suppose','assuming','providing','provided','in the event','just so','given','in case','on condition','as long as','as so long as']
        elif child_sentence[0] in ['if','whether','unless','supposing','suppose','assuming','providing','provided','in the event','just so','given','in case','on condition','as long as','as so long as']:
            Prefix_Adverbial_List.append(child_sentence)
            splited_sentence = splited_sentence[comma_index + 1:]

        # (10)前缀状语是 让步状语从句['though','thus','although','if','even','even though','even if','even though','whereas','whereas','whereas',granting','granted','admitting']
        elif child_sentence[0] in ['though','thus','although','if','even','even though','even if','even though','whereas','whereas','whereas','granting','granted','admitting']:
            Prefix_Adverbial_List.append(child_sentence)
            splited_sentence = splited_sentence[comma_index + 1:]

        #（）程度状语从句

        #（）目的状语从句

        #(11) 结果状语从句 一定位于主句之后
        else:
            continue

    return Prefix_Adverbial_List, splited_sentence

def get_suffix_adverbial_of_the_sentence(splited_sentence:list)->list:
    splited_sentence = splited_sentence
    Suffix_Adverbial_List = []
    Comma_Index_List = []
    # (1)先把句子中所有的逗号找出来并存在列表Comma_Index_List里
    for i in range(len(splited_sentence)):
        # 当前字符是英语中的逗号
        if splited_sentence[i] == "，":
            Comma_Index_List.append(i)
        else:
            continue

    for comma_index in Comma_Index_List[::-1]:
        child_sentence = splited_sentence[comma_index:-1:1]
        #(1)后缀to be
        if splited_sentence[comma_index+1]== 'to' and splited_sentence[comma_index+2]== 'be':
            Suffix_Adverbial_List.append(child_sentence)
            splited_sentence = splited_sentence[0:comma_index]+splited_sentence[-1]
            del Comma_Index_List[-1]

        #（2）后缀to+ 单性动词原型
        elif splited_sentence[comma_index + 1] in ['to'] and mydb.id_apple_verbpluspos_douuble_vori_vsimple(splited_sentence[i+2]):
            Suffix_Adverbial_List.append(child_sentence)
            splited_sentence = splited_sentence[0:comma_index]+splited_sentence[-1]
            del Comma_Index_List[-1]


        #（3）后缀to+ 多性动词原型

        #（4）非限制性定语从句

        #（5）让步状语从句

        #（6）条件状语从句


        else:
            continue

    #（1）with+名词+介词结构

    #（2）with+名词+单性动词或多性动词的现在分词

    #（3）其他后缀的介词结构

    #（4）时间状语从句

    #（5）条件状语从句

    #（6）地点状语从句

    #（7）让步状语从句

    pass
def get_adverbial_of_the_sentence(splited_sentence:list)->list:

    Adverbial_List=[]

    #(1)先把句子所有变成全部小写。
    splited_sentence.lower()

    #(2)分别找句子中的前缀状语和后缀状语
    Prefix_Adverbial_List=[]
    Suffix_Adverbial_List=[]
    Parenthetical_Phrase_List=[]
    Parenthetical_Phrase_List=parenthetical_phrase.get_parenthetical(splited_sentence)
    Prefix_Adverbial_List=get_prefix_adverbial_of_the_sentence(splited_sentence)
    Suffix_Adverbial_List=get_suffix_adverbial_of_the_sentence(splited_sentence)

    return Adverbial_List

if __name__ == '__main__':
    sentences=[]
    with open('adverbial_test.txt', 'r', encoding='utf-8') as f:
        for line in f:
            sentences.append(split_sentence_to_list.splited_sentence(line.strip()))
    print(sentences)


