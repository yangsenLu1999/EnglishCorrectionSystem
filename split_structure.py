import split_sentence_to_list
import judegclause
import mydb
import transfer_word
import attached_data_type
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

#查找当前列表中最靠前的主语结构


#如果是陈述句则主语一定在位于之前 predicate_beginning_index表示谓语的起始索引，可根据切分信号词缩小主语可能的范围
def use_split_singal_to_split_the_sentence(splited_sentence:list,predicate_beginnning_index:int)->list:
    # 非限制性定语从句同时是插入语解决方案：剔除“，”+“非限制性定语从句”+“，”三部分后，处理
    new_splited_sentence = splited_sentence[0:predicate_beginnning_index-1]
    for i in range(len(new_splited_sentence)):
        #(1)当前位置是to，且后一位是单性动词原型
        if i+1<len(new_splited_sentence) and new_splited_sentence[i] == 'to' and mydb.id_apple_verbpluspos_vori_vsimple(new_splited_sentence[i+1])>=0:
            new_splited_sentence=new_splited_sentence[i+1:]
            # return new_splited_sentence
        #当前位置是to,且后一位是多性动词原型
        elif i+1<len(new_splited_sentence) and new_splited_sentence[i]=="to" and mydb.id_apple_verbpluspos_double_vori_vcomplex(new_splited_sentence[i+1])>=0:
            new_splited_sentence=new_splited_sentence[i:]
            # return new_splited_sentence

        #(2)当前位置是介词
        elif mydb.id_apple_prep(new_splited_sentence[i])>=0:
            new_splited_sentence=new_splited_sentence[i:]
            # return new_splited_sentence

        #(3)当前位置是单性动词的现在分词或多性动词的现在分词
        elif mydb.id_apple_verbpluspos_vbg_vsimple(new_splited_sentence[i])>=0 or mydb.id_apple_verbpluspos_double_vbg_vcomplex(new_splited_sentence[i])>=0:
            new_splited_sentence=new_splited_sentence[i:]
            # return new_splited_sentence

        #（4）当前位置是英语句子中的关联词
        elif judegclause.is_a_conj_or_not(new_splited_sentence,i):
            new_splited_sentence = new_splited_sentence[i:]
            # return new_splited_sentence

        #(5)当前位置是英语句子中的标点符号
        elif new_splited_sentence[i] in ['.', '?', '!',',']:
            new_splited_sentence = new_splited_sentence[i:]
            # return new_splited_sentence
        else:
            pass
    return new_splited_sentence

#抓取句子中的主语,如果是陈述句则主语一定在位于之前 predicate_beginning_index表示谓语的起始索引。
def get_subject_DictList(splited_sentence:list,predicate_beginnning_index:int)->dict:
    Subject_Index_Dict = {'begin': 0, 'end': 0, 'subject': None}
    #(1)查看谓语前有无逗号。
    #当前版本不考虑“插入语”，非限制性定语从句同时是插入语解决方案：剔除“，”+“非限制性定语从句”+“，”三部分后，处理
    get_Subject_splited_sentence=splited_sentence[0:predicate_beginnning_index-1]
    #将句子中所有的单词变成小写
    new_splited_sentence =transfer_word.transfer_every_word_in_list_to_lower(get_Subject_splited_sentence)
    # 若谓语前无逗号，主语是离开谓语最远的主语组成结构
    if "," not in new_splited_sentence:
        for i in range(len(new_splited_sentence)):
            #(1）当前位置是人称代词主格、物主代词名词性、形容词性物主代词、指示代词、不定代词、相互代词
            if new_splited_sentence[i] in ['I','i','you','he','she','it','we','they'] or new_splited_sentence[i] in ['mine','yours','his','hers','its','ours','yours','theirs'] \
                    or new_splited_sentence[i] in ['my','your','his','her','its','our','your','their'] or new_splited_sentence[i] in ['this','that','these','those']\
                    or new_splited_sentence[i] in attached_data_type.inde_pron or new_splited_sentence[i] in attached_data_type.rec_pron\
                    or (i+1<len(new_splited_sentence) and (new_splited_sentence[i]+splited_sentence[i+1]) in attached_data_type.rec_pron):
                Subject_Index_Dict['begin'] = i
                Subject_Index_Dict['end'] = i
                Subject_Index_Dict['subject'] = new_splited_sentence[i]
                return Subject_Index_Dict
            #(2)当前位置是名词，前面是冠词['a','an','the']或量词或形容词性物主代词['my','your','his','her','their','our']或形容词原型或不带more的比较级或不带most的最高级
            elif mydb.id_apple_moun(new_splited_sentence[i])>=0:
                #查看前面的单词组合是否是冠词+副词+形容词+名词
                if i-3>=0 and new_splited_sentence[i-3] in ['a','an','the'] and mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(new_splited_sentence[i-2])>=0\
                    and mydb.id_apple_adjective_word_or_comparative_without_more_or_superlative_without_most(new_splited_sentence[i-1])>=0:
                    Subject_Index_Dict['begin'] = i-3
                    Subject_Index_Dict['end'] = predicate_beginnning_index-1
                    Subject_Index_Dict['subject'] = splited_sentence[i-3:predicate_beginnning_index-1]
                    return Subject_Index_Dict
                #查看前面的单词组合是否是形容词性物主代词+名词
                elif i-1>=0 and new_splited_sentence[i-1] in attached_data_type.adj_poss_pron:
                    Subject_Index_Dict['begin'] = i-1
                    Subject_Index_Dict['end'] = predicate_beginnning_index-1
                    Subject_Index_Dict['subject'] = splited_sentence[i-1:predicate_beginnning_index-1]
                    return Subject_Index_Dict
                #查看前面的单词组合是否是冠词+形容词+名词
                elif i-2>=0 and new_splited_sentence[i-2] in ['a','an','the'] and mydb.id_apple_adjective_word_or_comparative_without_more_or_superlative_without_most(new_splited_sentence[i-1])>=0:
                    Subject_Index_Dict['begin'] = i-2
                    Subject_Index_Dict['end'] = predicate_beginnning_index-1
                    Subject_Index_Dict['subject'] = splited_sentence[i-2:predicate_beginnning_index-1]
                    return Subject_Index_Dict
                #查看前面的单词组合是否是副词+形容词+名词
                elif i-2>=0 and mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(new_splited_sentence[i-2])>=0 and mydb.id_apple_adjective_word_or_comparative_without_more_or_superlative_without_most(new_splited_sentence[i-1])>=0:
                    Subject_Index_Dict['begin'] = i-2
                    Subject_Index_Dict['end'] = predicate_beginnning_index-1
                    Subject_Index_Dict['subject'] = splited_sentence[i-2:predicate_beginnning_index-1]
                    return Subject_Index_Dict
                #查看前面的单词组合是否是冠词+名词
                elif i-1>=0 and new_splited_sentence[i-1] in ['a','an','the']:
                    Subject_Index_Dict['begin'] = i-1
                    Subject_Index_Dict['end'] = predicate_beginnning_index-1
                    Subject_Index_Dict['subject'] = splited_sentence[i-1:predicate_beginnning_index-1]
                    return Subject_Index_Dict
                #查看前面的单词组合是否是量词+名词
                elif i-1>=0 and mydb.id_apple_quantifierlemma(new_splited_sentence[i-1])>=0:
                    Subject_Index_Dict['begin'] = i-1
                    Subject_Index_Dict['end'] = predicate_beginnning_index-1
                    Subject_Index_Dict['subject'] = splited_sentence[i-1:predicate_beginnning_index-1]
                    return Subject_Index_Dict
                else:
                    pass
            #（3）当前位置是to，且后一位是单性动词原型或多性动词原型
            elif new_splited_sentence[i] == 'to' and (mydb.id_apple_verbpluspos_vori_vsimple(new_splited_sentence[i+1])>=0 or mydb.id_apple_verbpluspos_double_vori_vcomplex(new_splited_sentence[i+1])>=0):
                Subject_Index_Dict['begin']=i
                Subject_Index_Dict['end']=predicate_beginnning_index-1
                Subject_Index_Dict['subject']=splited_sentence[i:predicate_beginnning_index-1]
            #（4）当前位置是单性动词的现在分词或多性动词的现在分词
            elif mydb.id_apple_verbpluspos_vbg_vsimple(new_splited_sentence[i])>=0 or mydb.id_apple_verbpluspos_double_vbg_vcomplex(new_splited_sentence[i])>=0:
                Subject_Index_Dict['begin']=i
                Subject_Index_Dict['end']=predicate_beginnning_index-1
                Subject_Index_Dict['subject']=splited_sentence[i:predicate_beginnning_index-1]
            #(5)当前位置是关联词
            elif judegclause.is_a_conj_or_not(new_splited_sentence,i):
                Subject_Index_Dict['begin']=i
                Subject_Index_Dict['end']=predicate_beginnning_index-1
                Subject_Index_Dict['subject']=splited_sentence[i:predicate_beginnning_index-1]
            else:
                pass
    # 若谓语前有逗号，主语是最后逗号后的第一个主语组成结构
    else:
        right_comma_index=-1
        for i in range(len(new_splited_sentence) - 1, -1, -1):
            if ',' in new_splited_sentence[i]:
                print(f"列表中最右边包含逗号的元素的索引为 {i}")
                right_comma_index=i
                break
            else:
                print("列表中没有包含逗号的元素")
        right_comma_to_predicate=new_splited_sentence[right_comma_index:]


    return Subject_Index_Dict

#抓取句子中的宾语和表语，表语认为是系动词后紧跟着的一位或几位，宾语认为是谓语结构紧跟着的下一位或下几位。
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
    # # print(splited_sentence[3]=="which")
    # splited_sentence,clause_list=get_rid_of_restrictive_clause(splited_sentence)
    # print(splited_sentence)
    # print(clause_list)
    # # splited_sentence=splited_sentence
    # # while i in splited_sentence:
    splited_sentence=use_split_singal_to_split_the_sentence(splited_sentence,5)
    print(splited_sentence)
