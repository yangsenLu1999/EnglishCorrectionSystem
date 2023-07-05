import split_sentence_to_list
import judegclause
import mydb
from collections import deque

#切分主语----------------------------------------------------------------------------------------------------------------
class Stack:
    def __init__(self):
        self.items = deque()  # 初始化一个空的双向队列

    def push(self, item):
        self.items.append(item)  # 将元素添加到队列尾部，即栈顶

    def pop(self):
        if not self.is_empty():
            return self.items.pop()  # 弹出队列尾部的元素，即栈顶
        else:
            return None  # 如果栈为空，则返回 None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]  # 返回队列尾部的元素，即栈顶（不弹出）
        else:
            return None  # 如果栈为空，则返回 None

    def size(self):
        return len(self.items)  # 返回栈的大小

    def is_empty(self):
        return len(self.items) == 0  # 判断栈是否为空

# #查找非限制性定语从句
# def find_non_restrictive_clause(sentence:list[str],splited_sentence:list[str]):
#     clauses = []
#     for i in range(len(sentence)):
#         if sentence[i] in [',', '。', '?', '!']:
#             clauses.append(sentence[:i])
#             sentence = sentence[i+1:]
#             break
#     clauses.append(sentence)
#     return clauses




#判断当前单词能不能组成主语结构
def use_split_singal_to_split_the_sentence(splited_sentence:list,i:int):
    #非限制性定语从句同时是插入语解决方案：剔除“，”+“非限制性定语从句”+“，”三部分后，处理
    splited_sentence=splited_sentence
    #(1)当前单词是to，且后一位是单性动词原型
    if i+1<len(splited_sentence) and splited_sentence[i] == 'to' and mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+1])>=0:
        splited_sentence=splited_sentence[i:]
        return splited_sentence
    #当前单词是to,且后一位是多性动词原型
    elif i+1<len(splited_sentence) and splited_sentence[i]=="to" and mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i+1])>=0:
        splited_sentence=splited_sentence[i:]
        return splited_sentence

    #(2)当前单词是介词
    elif mydb.id_apple_prep(splited_sentence[i])>=0:
        splited_sentence=splited_sentence[i:]
        return splited_sentence

    #(3)当前单词是单性动词的现在分词或多性动词的现在分词
    elif mydb.id_apple_verbpluspos_vbg_vsimple(splited_sentence[i])>=0 or mydb.id_apple_verbpluspos_double_vbg_vcomplex(splited_sentence[i])>=0:
        splited_sentence=splited_sentence[i:]
        return splited_sentence

    #(4)当前单词是单性动词的过去分词或多性动词的过去分词
    # 当前单词是否是关联词
    elif judegclause.is_a_conj_or_not(splited_sentence, i):
        splited_sentence = splited_sentence[i:]
        return splited_sentence



    #当前单词是单性动词的现在分词

    #当前单词是多性动词的现在分词

    #当前单词是单性动词的原型

    #当前单词是多性动词的原型
        return True
    else:
        return False
def get_subject_and_the_range(splited_sentence:list,begin_index_of_predicate:int,Subject_Index_Dict:dict)->dict:
    Subject_Index_Dict = {'begin': 0, 'end': 0, 'subjict': None}
    #(1)记录所有逗号的位置
    Comma_Index_List = []
    for i in range (len(splited_sentence)):
        if splited_sentence[i] == ',':
            Comma_Index_List.append(i)
    #(2）记录所有可能的主语组成结构
    SubjectStack = Stack()



    return Subject_Index_Dict


# if __name__ == '__main__':
