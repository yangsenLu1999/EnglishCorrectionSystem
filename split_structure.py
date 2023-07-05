import split_sentence_to_list
import judegclause
import mydb
from collections import deque

#切分主语----------------------------------------------------------------------------------------------------------------
#抓取非限制性定语从句，只找了一层
def get_rid_of_restrictive_clause(splited_sentence:list)->tuple:
    splited_sentence=splited_sentence
    clause_list=[]
    #若列表中没有逗号，肯定没有非限制性定语从句
    if "," not in splited_sentence:
        splited_sentence=splited_sentence
        clasue_list=[]
        return splited_sentence,clause_list
    else:
        for i in range(len(splited_sentence)):
            if splited_sentence[i] ==',' and i+1<=len(splited_sentence)-1 and splited_sentence[i+1] in ['who','whom','which','when','where','why','how']:
                #查看列表[i+1:]中有无逗号
                if "," not in splited_sentence[i+1:]:
                    clause_beginning_index_and_ending_index_tuple=(i,len(splited_sentence)-2)
                    clause_list.append(clause_beginning_index_and_ending_index_tuple)
                    splited_sentence=splited_sentence[0:i]+splited_sentence[-1:]
                    return splited_sentence,clause_list
                else:
                    for j in range(len(splited_sentence)-1,i,-1):
                        if splited_sentence[j] == ',':
                            clause_beginning_index_and_ending_index_tuple=(i,j)
                            clause_list.append(clause_beginning_index_and_ending_index_tuple)
                            splited_sentence=splited_sentence[0:i]+splited_sentence[j:]
                            return splited_sentence,clause_list
    #返回（除去非限制性定语从句的splited_sentence，(非限制性定语从句在原splited_sentence中的起始索引，非限制定语从句在元splited_sentence中的终止索引) )
    return  splited_sentence,clause_list

#根据切分信号缩小主语可能的范围
def use_split_singal_to_split_the_sentence(splited_sentence:list,i:int):
    #非限制性定语从句同时是插入语解决方案：剔除“，”+“非限制性定语从句”+“，”三部分后，处理
    splited_sentence=splited_sentence
    #(1)当前位置是to，且后一位是单性动词原型
    if i+1<len(splited_sentence) and splited_sentence[i] == 'to' and mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+1])>=0:
        splited_sentence=splited_sentence[i:]
        return splited_sentence
    #当前位置是to,且后一位是多性动词原型
    elif i+1<len(splited_sentence) and splited_sentence[i]=="to" and mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i+1])>=0:
        splited_sentence=splited_sentence[i:]
        return splited_sentence

    #(2)当前位置是介词
    elif mydb.id_apple_prep(splited_sentence[i])>=0:
        splited_sentence=splited_sentence[i:]
        return splited_sentence

    #(3)当前位置是单性动词的现在分词或多性动词的现在分词
    elif mydb.id_apple_verbpluspos_vbg_vsimple(splited_sentence[i])>=0 or mydb.id_apple_verbpluspos_double_vbg_vcomplex(splited_sentence[i])>=0:
        splited_sentence=splited_sentence[i:]
        return splited_sentence

    #（4）当前位置是英语句子中的关联词
    elif judegclause.is_a_conj_or_not(splited_sentence[i]):
        splited_sentence = splited_sentence[i:]
        return splited_sentence
    #(5)当前位置是英语句子中的标点符号
    elif splited_sentence[i] in ['.', '?', '!',',']:
        splited_sentence = splited_sentence[i:]
        return splited_sentence
    else:
        pass
    return splited_sentence

#抓取句子中的主语
def get_subject_DictList(splited_sentence:list)->dict:
    Subject_Index_Dict = {'begin': 0, 'end': 0, 'subject': None}
    subject_and_comma_tuple_list = []
    #(1)记录所有可能的主语位置和组成结构
    for i in range (len(splited_sentence)):
        #记录句子中的逗号和位置
        if splited_sentence[i] == ',':
            # Comma_Index_List.append(i)
            subject_and_comma_tuple=(i,",")
            subject_and_comma_tuple_list.append(subject_and_comma_tuple)
        elif True:
            pass
    return Subject_Index_Dict

#抓取句子中的宾语和表语
def get_predicative_and_object_DictList(splited_sentence:list)->list:
    predicative_and_object_DictList=[]
    pass
    return predicative_and_object_DictList

#抓取句子中的定语（包括普通定语和限制性定语从句）
# def get

if __name__ == '__main__':
    sentence = "a book,which I want to buy in the city where I spent my childhood."
    splited_sentence = split_sentence_to_list.splited_sentence(sentence)
    print(splited_sentence)
    # print(splited_sentence[3]=="which")
    splited_sentence,clause_list=get_rid_of_restrictive_clause(splited_sentence)
    print(splited_sentence)
    print(clause_list)
    # splited_sentence=splited_sentence
    # while i in splited_sentence:
