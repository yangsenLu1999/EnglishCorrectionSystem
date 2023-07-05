import collections
import mydb
import split_sentence_to_list
import judegclause

Predicate_Dictionary = collections.OrderedDict()

Predicate_Dictionary = collections.OrderedDict()
Predicate_Dictionary["priority_one"] = []
Predicate_Dictionary["priority_two"] = []
Predicate_Dictionary["priority_three"] = []
Predicate_Dictionary["priority_four"] = []

#信号词/关联词列表
CONJ_List = []

#信号词/关联词位置
CONJ_Location_List = []

#[(关联词1，关联词1的位置), (关联词2，关联词2的位置), (关联词3，关联词3的位置)]
CONJ_And_Location_Of_CONJ_List=[]

#已经配对好的谓语结构的索引,以元组的形式存储谓语结构的起始和终止
Begin_TO_End_Of_Predicate_List=[]

#当前优先级及以上优先级能找到的谓语结构
Priority_Now_And_Over_Predicate_List=[]

#最终句子的谓语结构（list里面的元素为字典{‘CONJn":'...',   'CONJ1’：'...' ,  '主句的谓语结构'：’...‘}）
Result_Predicate_List=[]

#情态动词
# vmodal=["can","could","cannot","may","might","must","shall","should","will","would"]
#双字符的情态动词单独处理  "ought","seem","have","used"

#将查到的可能的最长谓语写入res.txt
def write_into_restxt(longest_predicate):
    with open('../ex_predicate/res.txt', 'a') as f:
        f.write(longest_predicate+"\n")
    print("获取到了谓语结构：", longest_predicate)


#动词过去式的判别
def the_word_is_verb_past_tense_or_not(splited_sentence :list,i :int) ->bool:
    # (1)单词后是冠词articles = ['a', 'an', 'the']
    if i+1<len(splited_sentence) and splited_sentence[i+1] in ['a', 'an', 'the']:
        return True
    # (2)单词后为冠词和代词格(it,you另做判断),则直接判为过去式
    elif i+2<len(splited_sentence) and splited_sentence[i+2] in ['me', 'him', 'her', 'us', 'them', 'whom']:
        return True
    #(3)存在高优先级的谓语结构
    elif Priority_Now_And_Over_Predicate_List :
        return False

    #(4)being/having +(adv) 结构后为过去分词
    elif i-1>=0 and splited_sentence[i-1] in ['being', 'having']:
        return False
    elif i-2>=0 and splited_sentence[i-2] in ['being', 'having'] and mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i-1])>=0:
        return False

    #(5)过去式有名词词性，看单词前是否有the或者形容词,有则是名词
    elif i-1>=0 and (mydb.id_apple_moun(splited_sentence[i])>=0 or mydb.id_apple_adjective_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i-1])>=0):
        return False

    #(6)单词前有冠词，后有名词，则是动词过去分词
    elif i-1>=0 and splited_sentence[i-1] in ['a', 'an', 'the','A', 'An', 'The'] and i+1<len(splited_sentence) and mydb.id_apple_moun(splited_sentence[i+1])>=0 :
        return False

    #(7)位于句首是状语的引导词，则是动词过去分词
    elif i==0 :
        return False

    #(8)对于名词+过去式或过去分词+介词
    elif i-1>=0 and mydb.id_apple_moun(splited_sentence[i-1])>=0 and i+1<len(splited_sentence) and mydb.id_apple_prep(splited_sentence[i+1])>=0:
        #存在更高级的谓语结构,则是过去分词
        if Priority_Now_And_Over_Predicate_List:
            return False
        else:
            return True
    else:
        return True

#多性动词的判别
def the_word_is_vcomplex_and_work_as_verb_or_not(splited_sentence:list,i:int)->bool:  #该单词是一个多性动词且在此处有动词词性
    # 该单词在多性动词表中可以查询到，是一个多性动词
    if mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i])>=0 \
        or mydb.id_apple_verbpluspos_double_vbz_vcomplex(splited_sentence[i])>=0\
        or mydb.id_apple_verbpluspos_double_vbg_vcomplex(splited_sentence[i])>=0\
        or mydb.id_apple_verbpluspos_double_vbd_vcomplex(splited_sentence[i])>=0\
        or mydb.id_apple_verbpluspos_double_vbn_vcomplex(splited_sentence[i])>=0:

        #(1)Adj. （包括形容词性从句关联词：i.e whose）+ V多 （the+adj除外）
        if i-1>=0 and splited_sentence[i-1] in ["whose",'Whose']:
            return False
        elif i-1>=0 and mydb.id_apple_adjective_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i-1])>=0:
            return False

        #(2)Prep + v多
        ##前面一个单词存在且是介词
        elif i-1>=0 and mydb.id_apple_prep(splited_sentence[i-1])>=0 :
            return False

        #(3)Much/more + v多
        #前面一个单词存在且是much/more
        elif i-1>=0 and splited_sentence[i-1] in ['much','more','Much','More']:
            return False

        #(4)冠词/量词 + v多
        elif i-1>=0 and splited_sentence[i-1] in ['a', 'an', 'the','A', 'An', 'The']:
            return False
        elif i-1>=0 and mydb.id_apple_quantifierlemma(splited_sentence[i-1])>=0:
            return False

        #(5)高级别谓语结构 + v多

        # (6)人称 / 物主代词 / 宾格 + v多(it, you另做判断)出现'you'和'it' + V多时，判断you / it前面的单词，如果是介词或动词（do / be), 那么you / it是宾格
        elif i-1>=0 and splited_sentence[i-1] in ['me','him','her','us','them','my','your','our','his','her','its','theirs','My','Your','Our','His','Her','Its','Theirs']:
            return False
        elif i-1>=0 and splited_sentence[i-1] in ['you','it','It','You']:
            #it/you 前面是单性动词
            if i-2>=0 and ( mydb.id_apple_prep(splited_sentence[i-2]) >=0 or mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i-2])>=0 \
                            or mydb.id_apple_verbpluspos_vbz_vsimple(splited_sentence[i-2])>=0 \
                            or mydb.id_apple_verbpluspos_vbg_vsimple(splited_sentence[i-2])>=0 \
                            or mydb.id_apple_verbpluspos_vbd_vsimple(splited_sentence[i-2])>=0 \
                            or mydb.id_apple_verbpluspos_vbn_vsimple(splited_sentence[i-2])>=0):
                return False

        #(7)n单数 + v多原形
        elif  i-1>=0 and  mydb.id_apple_moun_noun_origin(splited_sentence[i-1])>=0 and mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i])>=0:
            return False
        #(8)n复数 + v多三单   （n为men/women除外）
        elif  i-1>=0 and  mydb.id_apple_moun_noun_plural(splited_sentence[i-1])>=0 and splited_sentence[i-1]!=['men','women'] and mydb.id_apple_verbpluspos_double_vbz_vcomplex(splited_sentence[i])>=0:
            return False

    return True

#查看是否满足优先级别一.1
#1.情态动词+（adv）动词原形：can do；will do；should really do
def check_priority_one_one(splited_sentence,i):
    predicate = ""
    # 优先级别一：
    if splited_sentence[i] in ["can","could","cannot","may","might","must","shall","should","will","would",'need'] :  # 该词语是一个情态动词
        #（1）情态动词+not+副词原型或不带more的比较级或不带most的最高级+单性动词或多性动词原型：
        #后一位是not #后两位是副词原型或不带more的比较级或不带most的最高级 #后三位是单性动词原型或多性动词的原型
        if i+1<len(splited_sentence) and splited_sentence[i+1]== "not" and i+2<len(splited_sentence) and mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+2])>=0 and i+3<len(splited_sentence)and (mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+3]) >=0 or mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i+3])>=0):
            predicate=splited_sentence[i]+" "+splited_sentence[i+1]+" "+splited_sentence[i+2]+" "+splited_sentence[i+3]
            return predicate

        #（2）情态动词+not或副词原型或不带more的比较级或不带most的最高级+单性动词原型或多性动词原形
        #后一位是not或者副词原型或不带more的比较级或不带most的最高级 #后两位是单性动词原形或者多性动词原型
        elif i+1<len(splited_sentence) and (splited_sentence[i+1]=='not' or mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+1])>=0) and i+2<len(splited_sentence) and (mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+2])>=0 or mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i+2])>=0):
            predicate=splited_sentence[i]+" "+splited_sentence[i+1]+" "+splited_sentence[i+2]
            return predicate

        # (3)情态动词+be+单性动词的过去分词或多性动词的过去分词
        elif i + 2 < len(splited_sentence) and splited_sentence[i + 1] == 'be' and (mydb.id_apple_verbpluspos_vbn_vsimple(splited_sentence[i + 2]) >= 0 or mydb.id_apple_verbpluspos_double_vbn_vcomplex(splited_sentence[i + 2]) >= 0):
            predicate = splited_sentence[i] + " " + splited_sentence[i + 1] + " " + splited_sentence[i + 2]
            return predicate

        #（4）情态动词+单性动词原型或者多性动词原形
        elif i+1<len(splited_sentence) and (mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+1])>=0 or mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i+1])>=0):
            predicate=splited_sentence[i]+" "+splited_sentence[i+1]
            return predicate



        else:
            pass

    #当前单词与后一个单词组成了情态动词（to）
    elif splited_sentence[i] in ['have','used','ought','seem'] and i+1<=len(splited_sentence)-1 and splited_sentence[i+1]=='to':
        #（1）情态动词（to）+not+副词原型或不带more的比较级或不带most的最高级+单性动词或多性动词原型：
        #后两位为not #后三位为副词原型或不带more的比较级或不带most的最高级
        if i+2<len(splited_sentence) and splited_sentence[i+2]== "not" and i+3<len(splited_sentence)and mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+3])>=0 and i+4<len(splited_sentence)and (mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+4])>=0 or mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i+4])>=0):
            predicate=splited_sentence[i]+" "+splited_sentence[i+2]+" "+splited_sentence[i+3]+" "+splited_sentence[i+4]
            return predicate

        #(2)情态动词（to）+not或副词原型或不带more的比较级或不带most的最高级+单性动词原型或多性动词原型
        elif i+2<len(splited_sentence) and (splited_sentence[i+2]=='not' or mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+2])>=0) and i+3<len(splited_sentence)and (mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+3])>=0 or mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i+3])>=0):
            predicate=splited_sentence[i]+" "+splited_sentence[i+2]+" "+splited_sentence[i+3]
            return predicate

        #（3）情态动词（to）+单性动词原型或者多性动词原型
        elif i+2<len(splited_sentence) and (mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+2])>=0 or mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i+2])>=0):
            predicate=splited_sentence[i]+" "+splited_sentence[i+2]
        else:
            pass
    else:
        pass

    return predicate

#查看是否满足优先级别一.2
#2.助动词（do）+（adv）动词原形：do not like；did like；does like
def check_priority_one_two(splited_sentence,i):
    predicate =""
    if splited_sentence[i] in ["do","does","did"]:  # 该词语是一个do/did/does
        #（1）do/did/does+not+副词原型或者不带more的比较级或不带most的最高级+单性动词原型或多性动词原型
        if i+1<len(splited_sentence) and splited_sentence[i+1]=='not' and i+2<len(splited_sentence) and mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+2])>=0 and i+3<len(splited_sentence)and (mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+3])>=0 or mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i+3])>=0):
            predicate=splited_sentence[i]+" "+splited_sentence[i+1]+" "+splited_sentence[i+2]+" "+splited_sentence[i+3]
            return predicate

        #(2)do/did/does+not或副词原型或者不带more的比较级或不带most的最高级+单性动词原型或多性动词原型
        elif i+1<len(splited_sentence) and (splited_sentence[i+1]=='not' and mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+1])>=0) and i+2<len(splited_sentence) and (mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+2])>=0 or mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i+2])>=0):
            predicate=splited_sentence[i]+' '+splited_sentence[i+1]+' '+splited_sentence[i+2]

        #(3)do/did/does+单性动词原型或多性动词原型
        elif i+1<len(splited_sentence) and (mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+1])>=0 or mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i+1])>=0 ):
            predicate=splited_sentence[i]+' '+splited_sentence[i+1]
    else:
        pass

    return predicate


#查看是否满足优先级别一.3
#3.am/is/are/was/were +（adv）done/doing：are doing；is done
def check_priority_one_three(splited_sentence,i):
    predicate =""
    # 该词语是一个am is are was were
    if splited_sentence[i] in ["am","is","are","was","were"]:
        # (1)am is are was were+副词原型或不带more的比较级或不带most的最高级+单性动词的现在分词（构成或不构成动词词组）
        #i+1 副词原型或不带more的比较级或不带most的最高级 #i+2 单性动词的现在分词
        if i+1<len(splited_sentence) and mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+1])>=0 and i+2<len(splited_sentence) and (mydb.id_apple_verbpluspos_vbg_vsimple(splited_sentence[i+2])>=0):
            # 单性动词的现在分词且组成动词词组
            if i+3<len(splited_sentence) and mydb.id_apple_fixedmatch_vbg(splited_sentence,i+2)>=0:
                predicate=splited_sentence[i]+" "+splited_sentence[i+1]+" "+splited_sentence[i+2]+" "+splited_sentence[i+3]
                return predicate
            #单性动词的现在分词且不组成动词词组
            elif i+3<len(splited_sentence) and mydb.id_apple_fixedmatch_vbg(splited_sentence,i+2)<0:
                predicate=splited_sentence[i]+" "+splited_sentence[i+1]+" "+splited_sentence[i+2]
                return predicate
            #其他
            else:
                pass

        # (2)am is are was were+单性动词的现在分词（构成或不构成动词词组）
        elif i+1<len(splited_sentence) and mydb.id_apple_verbpluspos_vbg_vsimple(splited_sentence[i+1])>=0:
            #单性动词的现在分词可以组成动词词组
            if i+2<len(splited_sentence) and mydb.id_apple_fixedmatch_vbg(splited_sentence,i+1)>=0:
                predicate=splited_sentence[i]+" "+splited_sentence[i+1]+" "+splited_sentence[i+2]
                return predicate
            #单性动词的现在分词不能组成动词词组
            elif i+2<len(splited_sentence) and mydb.id_apple_fixedmatch_vbg(splited_sentence,i+1)<0:
                predicate=splited_sentence[i]+" "+splited_sentence[i+1]
                return predicate
            #其他
            else:
                pass

        # (3)am is are was were+副词原型或不带more的比较级或不带most的最高级+多性动词的现在分词（构成或不构成动词词组)
        # i+2是多性动词的现在分词
        elif i+1<len(splited_sentence) and mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+1])>=0 and i+2<len(splited_sentence) and mydb.id_apple_verbpluspos_double_vbg_vcomplex(splited_sentence[i+2])>=0:
            #多性动词的现在分词可以组成动词词组
            if i+3<len(splited_sentence) and mydb.id_apple_fixedmatch_vbg(splited_sentence,i+2)>=0:
                predicate=splited_sentence[i]+" "+splited_sentence[i+1]+" "+splited_sentence[i+2]+" "+splited_sentence[i+3]
                return predicate
            #多性动词的现在分词不能组成动词词组
            elif i+3<len(splited_sentence) and mydb.id_apple_fixedmatch_vbg(splited_sentence,i+2)<0:
                predicate=splited_sentence[i]+" "+splited_sentence[i+1]+" "+splited_sentence[i+2]
                return predicate
            #其他
            else:
                pass

         #（4）am is are was were+多性动词的现在分词（构成或不构动词词组）
        elif i+1<len(splited_sentence) and mydb.id_apple_verbpluspos_double_vbg_vcomplex(splited_sentence[i+1])>=0:
            #多性动词的现在分词可以组成动词词组
            if i+2<len(splited_sentence) and mydb.id_apple_fixedmatch_vbg(splited_sentence,i+1)>=0:
                predicate=splited_sentence[i]+" "+splited_sentence[i+1]+" "+splited_sentence[i+2]
                return predicate
            #多性动词的现在分词不能组成动词词组
            elif i+2<len(splited_sentence) and mydb.id_apple_fixedmatch_vbg(splited_sentence,i+1)<0:
                predicate=splited_sentence[i]+" "+splited_sentence[i+1]
                return predicate
        # #(5)----------------------------------------------------------------------------------------
        # (5)am is are was were+副词原型或不带more的比较级或不带most的最高级+单性动词的过去分词（构成或不构成动词词组）
        # i+1 副词原型或不带more的比较级或不带most的最高级 #i+2 单性动词的过去分词
        elif i + 1 < len(
                splited_sentence) and mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(
                splited_sentence[i + 1]) >= 0 and i + 2 < len(splited_sentence) and (
                mydb.id_apple_verbpluspos_vbn_vsimple(splited_sentence[i + 2]) >= 0):
            # 单性动词的过去分词且组成动词词组
            if i + 3 < len(splited_sentence) and mydb.id_apple_fixedmatch_vbn(splited_sentence, i + 2) >= 0:
                predicate = splited_sentence[i] + " " + splited_sentence[i + 1] + " " + splited_sentence[
                    i + 2] + " " + splited_sentence[i + 3]
                return predicate
            # 单性动词的过去分词且不组成动词词组
            elif i + 3 < len(splited_sentence) and mydb.id_apple_fixedmatch_vbn(splited_sentence, i + 2) < 0:
                predicate = splited_sentence[i] + " " + splited_sentence[i + 1] + " " + splited_sentence[i + 2]
                return predicate
            # 其他
            else:
                pass

        # (6)am is are was were+单性动词的过去分词（构成或不构成动词词组）
        elif i + 1 < len(splited_sentence) and mydb.id_apple_verbpluspos_vbn_vsimple(splited_sentence[i + 1]) >= 0:
            # 单性动词的过去分词可以组成动词词组
            if i + 2 < len(splited_sentence) and mydb.id_apple_fixedmatch_vbn(splited_sentence, i + 1) >= 0:
                predicate = splited_sentence[i] + " " + splited_sentence[i + 1] + " " + splited_sentence[i + 2]
                return predicate
            # 单性动词的过去分词不能组成动词词组
            elif i + 2 < len(splited_sentence) and mydb.id_apple_fixedmatch_vbn(splited_sentence, i + 1) < 0:
                predicate = splited_sentence[i] + " " + splited_sentence[i + 1]
                return predicate
            # 其他
            else:
                pass

        # (7)am is are was were+副词原型或不带more的比较级或不带most的最高级+多性动词的过去分词（构成或不构成动词词组)
        # i+2是多性动词的过去分词
        elif i + 1 < len(
                splited_sentence) and mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(
                splited_sentence[i + 1]) >= 0 and i + 2 < len(
                splited_sentence) and mydb.id_apple_verbpluspos_double_vbn_vcomplex(splited_sentence[i + 2]) >= 0:
            # 多性动词的过去分词可以组成动词词组
            if i + 3 < len(splited_sentence) and mydb.id_apple_fixedmatch_vbn(splited_sentence, i + 2) >= 0:
                predicate = splited_sentence[i] + " " + splited_sentence[i + 1] + " " + splited_sentence[
                    i + 2] + " " + splited_sentence[i + 3]
                return predicate
            # 多性动词的过去分词不能组成动词词组
            elif i + 3 < len(splited_sentence) and mydb.id_apple_fixedmatch_vbn(splited_sentence, i + 2) < 0:
                predicate = splited_sentence[i] + " " + splited_sentence[i + 1] + " " + splited_sentence[i + 2]
                return predicate
            # 其他
            else:
                pass

        # （8）am is are was were+多性动词的过去分词（构成或不构动词词组）
        elif i + 1 < len(splited_sentence) and mydb.id_apple_verbpluspos_double_vbn_vcomplex(
                splited_sentence[i + 1]) >= 0:
            # 多性动词的过去分词可以组成动词词组
            if i + 2 < len(splited_sentence) and mydb.id_apple_fixedmatch_vbn(splited_sentence, i + 1) >= 0:
                predicate = splited_sentence[i] + " " + splited_sentence[i + 1] + " " + splited_sentence[i + 2]
                return predicate
            # 多性动词的过去分词不能组成动词词组
            elif i + 2 < len(splited_sentence) and mydb.id_apple_fixedmatch_vbn(splited_sentence, i + 1) < 0:
                predicate = splited_sentence[i] + " " + splited_sentence[i + 1]
                return predicate
    return predicate

#查看是否满足优先级别一.4
#4.动词过去式（百分百为过去式，没有原形/过去分词等其他词性）：did；wrote
def check_priority_one_four(splited_sentence,i):
    predicate=""
    #是单性动词的过去式且不可能是原型 三单 过去分词
    for index in mydb.dictionary_of_apple_verbpluspos:
        if splited_sentence[i] == mydb.dictionary_of_apple_verbpluspos[index]['vbd'] and splited_sentence[i]!=mydb.dictionary_of_apple_verbpluspos[index]\
            and splited_sentence[i]!=mydb.dictionary_of_apple_verbpluspos[index]['vbz'] and splited_sentence[i]!=mydb.dictionary_of_apple_verbpluspos[index]['vbg'] \
            and splited_sentence[i]!=mydb.dictionary_of_apple_verbpluspos[index]['vbn']:
            predicate=splited_sentence[i]
    return predicate

#查看是否满足优先级别二.1
#1.单性动词原形和三单：
def check_priority_two_one(splited_sentence,i):
    predicate=""
    #单性动词的原型或三单
    if mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i])>=0 or mydb.id_apple_verbpluspos_vbz_vsimple(splited_sentence[i])>=0:
        # print(mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i]),mydb.id_apple_verbpluspos_vbz_vsimple(splited_sentence[i]))
        predicate=splited_sentence[i]
    return predicate

#查看是否满足优先级别二.2

#2. have/had/has +（adv）done：have been done
def check_priority_two_two(splited_sentence,i):
    predicate=""
    if splited_sentence[i] in ["have","had","has"]:  # 该词语是一个have had has
        # (1)have/has/had +单性动词的过去分词或多性动词的过去分词
        if i+1<len(splited_sentence) and (mydb.id_apple_verbpluspos_vbn_vsimple(splited_sentence[i+1])>=0 or mydb.id_apple_verbpluspos_double_vbn_vcomplex(splited_sentence[i+1])>=0):
            predicate=splited_sentence[i]+" "+splited_sentence[i+1]
        # (2)have/has/had +副词原型或不带more的比较级或不带most的最高级+单性动词的过去分词或多性动词的过去分词
        elif i+2<len(splited_sentence) and mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+1])>=0 and  (mydb.id_apple_verbpluspos_vbn_vsimple(splited_sentence[i+2])>=0 or mydb.id_apple_verbpluspos_double_vbn_vcomplex(splited_sentence[i+2])>=0 or splited_sentence[i+2]=='been'):
            predicate=splited_sentence[i]+" "+splited_sentence[i+1]+" "+splited_sentence[i+2]
        else:
            pass
    else:
        pass
    return predicate

#查看是否满足优先级别三.1
#1.动词过去式（区分是否为动词过去分词或其他（除n + vbd + prep））：proposed
def check_priority_three_one(splited_sentence,i):
    predicate=""
    #(1)除了名词+单性动词或多性动词的过去式+介词
    if i-1<=0 and mydb.id_apple_moun(splited_sentence[i-1])>=0 and ( mydb.id_apple_verbpluspos_vbd_vsimple(splited_sentence[i]) >=0 or mydb.id_apple_verbpluspos_double_vbd_vcomplex(splited_sentence[i])>=0) and i+1<len(splited_sentence)and mydb.id_apple_prep(splited_sentence[i+1])>=0:
        return predicate

    #(2)单性动词过去式或多性动词过去式
    elif  (mydb.id_apple_verbpluspos_vbd_vsimple(splited_sentence[i]) >=0 or mydb.id_apple_verbpluspos_double_vbd_vcomplex(splited_sentence[i])>=0) and the_word_is_verb_past_tense_or_not(splited_sentence,i):
        predicate = splited_sentence[i]  # 将谓语结构拼接出来

    # #?????????????????????????
    # # (1)am is are was were+not
    # elif i+1<len(splited_sentence) and splited_sentence[i] in ["am","is","are","was","were"] and splited_sentence[i+1]=='not':
    #     predicate = splited_sentence[i]+' '+splited_sentence[i+1]+' '+splited_sentence[i+2]
    #     return predicate
    # #(2)am is are was were
    # elif i+1<len(splited_sentence) and splited_sentence[i] in ["am","is","are","was","were"]:
    #     predicate = splited_sentence[i]+' '+splited_sentence[i+1]
    #     return predicate
    else:
        pass
    return predicate

#查看是否满足优先级别三.2
#2.多性动词原形和三单（区分是否为名词或其他）：respect
def check_priority_three_two(splited_sentence,i):
    predicate=""
    # 是多性动词的原型或多性动词的三单  (区分是否为名词或其他)
    if (mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i])>=0 or mydb.id_apple_verbpluspos_double_vbz_vcomplex(splited_sentence[i])>=0) and the_word_is_vcomplex_and_work_as_verb_or_not(splited_sentence,i):
        predicate=splited_sentence[i]
    return predicate

def check_priority_be_not(splited_sentence,i):
    predicate=""
    if splited_sentence[i] in['am','is','are','was','were'] and i+1<len(splited_sentence) and splited_sentence[i+1]=='not':
        predicate=splited_sentence[i]+' '+splited_sentence[i+1]
    elif splited_sentence[i] in ['am','is','are','was','were']:
        predicate=splited_sentence[i]
    else:
        pass
    return predicate

#查看是否满足优先级别四.1
#1.动词过去式（n + vbd + prep）：The car moved in the morning
def check_priority_four_one(splited_sentence,i):
    predicate=""
    # (1)名词+单性动词或多性动词的过去式+介词
    if i+2<= len(splited_sentence)-1 and mydb.id_apple_moun(splited_sentence[i]) >= 0 and (mydb.id_apple_verbpluspos_vbd_vsimple(
            splited_sentence[i+1]) >= 0 or mydb.id_apple_verbpluspos_double_vbd_vcomplex(
            splited_sentence[i+1]) >= 0) and mydb.id_apple_prep(
            splited_sentence[i + 2]) >= 0:
        predicate = splited_sentence[i] + " " + splited_sentence[i+1] + " " + splited_sentence[i + 2]
        return predicate
    else:
        pass
    return predicate



#谓语结构的抽取
def extract_predicate(splited_sentence):
    global CONJ_List
    global CONJ_Location_List
    global CONJ_And_Location_Of_CONJ_List
    global Begin_TO_End_Of_Predicate_List
    global Priority_Now_And_Over_Predicate_List
    global Result_Predicate_List
    global Predicate_Dictionary

    #(1)先从头到尾部扫描出从句关联词和从句关联词的位置,将其以（CONJ,INDEX）的元组形式存储在CONJ_and_location_of_CONJ里
    for i in range(len(splited_sentence)):
        #当前位置是关联词
        if judegclause.is_a_conj_or_not(splited_sentence,i):
            CONJ_Location_Tuple=(splited_sentence[i],i)
            CONJ_And_Location_Of_CONJ_List.append(CONJ_Location_Tuple)
            #将CONJ存储到信号词/关联词列表里
            CONJ_List.append(splited_sentence[i])
            #将CONJ的位置存储到信号词/关联词位置列表里
            CONJ_Location_List.append(i)
        else:
            continue

    # (2)先处理句子中的插入语
    # ？？？？？？？？？？？？？
    # 先识别出句子的插入语，然后对插入语进行判断。如果是从句关联词引导的插入语，则单独对插入语进行谓语结构抓取，按照优先级一到四抓取谓语结构，抓到了以{‘关联词’,‘谓语结构’}的格式存储在Result_Predicate_List里
    # 找不到则以{’关联词’,‘None’}的格式存储在Result_Predicate_List里。如果不是，则跳过。

    # (3)先抓取从句的谓语结构，默认为None，根据信号词逐行扫描。从关联词到,或.    按照优先级一到四抓取谓语结构，抓到了以{‘关联词’,‘谓语结构’}的格式存储在Result_Predicate_List里找不到则以{’关联词’,‘None’}的格式存储在Result_Predicate_List里。
    #_______________________________________________________________________________________

    for Tuple_item in CONJ_And_Location_Of_CONJ_List[::-1]:
       Singal = False
       #CONJ是关联词，index是此关联词的位置。
       CONJ,index=Tuple_item

       for i in range(index+1,len(splited_sentence),1):
           End_Simgle_List=[',','.']
           #遍历到结束符号
           if splited_sentence[i] in End_Simgle_List:
               break
           elif i in CONJ_Location_List:
               break
           else:
               #优先级一
               #在当前位置i前面是‘to’或'To'
               if i-1>=0 and splited_sentence[i-1] in ['to','To']:
                   continue
               predicate_one_one=check_priority_one_one(splited_sentence,i)
               predicate_one_two=check_priority_one_two(splited_sentence,i)
               predicate_one_three=check_priority_one_three(splited_sentence,i)
               predicate_one_four=check_priority_one_four(splited_sentence,i)
               Predicate_Priority_One_List=[]
               #将优先级一到四抓取的谓语结构放入Predicate_Priority_One_List里
               Predicate_Priority_One_List.append(predicate_one_one)
               Predicate_Priority_One_List.append(predicate_one_two)
               Predicate_Priority_One_List.append(predicate_one_three)
               Predicate_Priority_One_List.append(predicate_one_four)
               predicate=max(Predicate_Priority_One_List,key=len)
               #如果优先级一所抓取到的谓语结构不为空且不在Begin_TO_End_Of_Predicate_List里
               Begin_To_End_Tuple=(i,i+len(predicate)-1)
               if predicate and Begin_To_End_Tuple not in Begin_TO_End_Of_Predicate_List:
                   #将已经配对好的谓语结构的起始和终止存储在Begin_To_End_Of_Predicate_List里
                   Begin_TO_End_Of_Predicate_List.append(Begin_To_End_Tuple)
                   # 当前优先级及以上优先级能找到的谓语结构
                   Priority_Now_And_Over_Predicate_List.append(predicate)
                   # 最终句子的谓语结构（list里面的元素为字典{‘CONJn":'...',   'CONJ1’：'...' ,  '主句的谓语结构'：’...‘}）
                   my_dict={}
                   my_dict[CONJ]=predicate
                   Result_Predicate_List.append(my_dict)
                   Singal=True
                   break
               else:
                  continue

       if not Singal:
            #2)按照优先级2抓取谓语结构
            #-----------------------------------------------------------------------
            for i in range(index + 1, len(splited_sentence), 1):
                End_Simgle_List = [',', '.'] + CONJ_List
                # 没有遍历到结束符号
                if splited_sentence[i] in End_Simgle_List:
                    break
                else:
                    # 优先级二
                    # 在当前位置i
                    # 在当前位置i前面是‘to’或'To'
                    if i - 1 >= 0 and splited_sentence[i - 1] in ['to', 'To']:
                        continue
                    predicate_two_one = check_priority_two_one(splited_sentence, i)
                    predicate_two_two = check_priority_two_two(splited_sentence, i)
                    Predicate_Priority_Two_List = []
                    Predicate_Priority_Two_List.append(predicate_two_one)
                    Predicate_Priority_Two_List.append(predicate_two_two)
                    predicate = max(Predicate_Priority_Two_List,key=len)
                    # 如果优先级二所抓取到的谓语结构不为空且不在Begin_TO_End_Of_Predicate_List里
                    Begin_To_End_Tuple = (i, i + len(predicate) - 1)
                    if predicate and Begin_To_End_Tuple not in Begin_TO_End_Of_Predicate_List:
                        # 将已经配对好的谓语结构的起始和终止存储在Begin_To_End_Of_Predicate_List里
                        Begin_TO_End_Of_Predicate_List.append(Begin_To_End_Tuple)
                        # 当前优先级及以上优先级能找到的谓语结构
                        Priority_Now_And_Over_Predicate_List.append(predicate)
                        # 最终句子的谓语结构（list里面的元素为字典{‘CONJn":'...',   'CONJ1’：'...' ,  '主句的谓语结构'：’...‘}）
                        my_dict = {}
                        my_dict[CONJ] = predicate
                        Result_Predicate_List.append(my_dict)
                        Singal = True
                        break
                    else:
                        continue

       if not Singal:
            #3)按照优先级三抓取谓语结构
            #-----------------------------------------------------------------------
            for i in range(index + 1, len(splited_sentence), 1):
                End_Simgle_List = [',', '.'] + CONJ_List
                # 没有遍历到结束符号
                if splited_sentence[i] in End_Simgle_List:
                    break
                else:
                    # 优先级三
                    # 在当前位置i
                    # 在当前位置i前面是‘to’或'To'
                    if i - 1 >= 0 and splited_sentence[i - 1] in ['to', 'To']:
                        continue
                    predicate_three_one = check_priority_three_one(splited_sentence, i)
                    # predicate_be_not = check_priority_be_not(splited_sentence, i)
                    predicate_three_two = check_priority_three_two(splited_sentence, i)
                    Predicate_Priority_Three_List = []
                    Predicate_Priority_Three_List.append(predicate_three_one)
                    # Predicate_Priority_Three_List.append(predicate_be_not)
                    Predicate_Priority_Three_List.append(predicate_three_two)
                    predicate = max(Predicate_Priority_Three_List,key=len)
                    # 如果优先级二所抓取到的谓语结构不为空且不在Begin_TO_End_Of_Predicate_List里
                    Begin_To_End_Tuple = (i, i + len(predicate) - 1)
                    if predicate and Begin_To_End_Tuple not in Begin_TO_End_Of_Predicate_List:
                        # 将已经配对好的谓语结构的起始和终止存储在Begin_To_End_Of_Predicate_List里
                        Begin_TO_End_Of_Predicate_List.append(Begin_To_End_Tuple)
                        # 当前优先级及以上优先级能找到的谓语结构
                        Priority_Now_And_Over_Predicate_List.append(predicate)
                        # 最终句子的谓语结构（list里面的元素为字典{‘CONJn":'...',   'CONJ1’：'...' ,  '主句的谓语结构'：’...‘}）
                        my_dict = {}
                        my_dict[CONJ] = predicate
                        Result_Predicate_List.append(my_dict)
                        Singal = True
                        break
                    else:
                        continue

       if not Singal:
           #（4）按照优先级四抓取谓语结构
           #-----------------------------------------------------------------------
            for i in range(index + 1, len(splited_sentence), 1):
                End_Simgle_List = [',', '.'] + CONJ_List
                # 没有遍历到结束符号
                if splited_sentence[i] in End_Simgle_List:
                    break
                else:
                    # 优先级四
                    # 在当前位置i
                    # 在当前位置i前面是‘to’或'To'
                    if i - 1 >= 0 and splited_sentence[i - 1] in ['to', 'To']:
                        continue
                    predicate_four_one = check_priority_four_one(splited_sentence, i)
                    Predicate_Priority_Four_List = []
                    # 如果优先级二所抓取到的谓语结构不为空且不在Begin_TO_End_Of_Predicate_List里
                    Begin_To_End_Tuple = (i, i + len(predicate) - 1)
                    if predicate and Begin_To_End_Tuple not in Begin_TO_End_Of_Predicate_List:
                        # 将已经配对好的谓语结构的起始和终止存储在Begin_To_End_Of_Predicate_List里
                        Begin_TO_End_Of_Predicate_List.append(Begin_To_End_Tuple)
                        # 当前优先级及以上优先级能找到的谓语结构
                        Priority_Now_And_Over_Predicate_List.append(predicate)
                        # 最终句子的谓语结构（list里面的元素为字典{‘CONJn":'...',   'CONJ1’：'...' ,  '主句的谓语结构'：’...‘}）
                        my_dict = {}
                        my_dict[CONJ] = predicate
                        Result_Predicate_List.append(my_dict)
                        Singal = True
                        break
                    else:
                        continue
       if not Singal:
           my_dict={}
           my_dict[CONJ]=None
           Result_Predicate_List.append(my_dict)
       Priority_Now_And_Over_Predicate_List.clear()

    # #(4)抓取主句的谓语结构
    Singal_Main=False
    for i in range(len(splited_sentence)):
        # 优先级一
        # 在当前位置i
        # 在当前位置i前面是‘to’或'To'
        if i - 1 >= 0 and splited_sentence[i - 1] in ['to', 'To']:
            continue
        predicate_one_one = check_priority_one_one(splited_sentence, i)
        predicate_one_two = check_priority_one_two(splited_sentence, i)
        predicate_one_three = check_priority_one_three(splited_sentence, i)
        predicate_one_four = check_priority_one_four(splited_sentence, i)
        Predicate_Priority_One_List = []
        # 将优先级一到四抓取的谓语结构放入Predicate_Priority_One_List里
        Predicate_Priority_One_List.append(predicate_one_one)
        Predicate_Priority_One_List.append(predicate_one_two)
        Predicate_Priority_One_List.append(predicate_one_three)
        Predicate_Priority_One_List.append(predicate_one_four)
        predicate = max(Predicate_Priority_One_List, key=len)
        # 如果优先级一所抓取到的谓语结构不为空且不在Begin_TO_End_Of_Predicate_List里
        Begin_To_End_Tuple = (i, i + len(predicate) - 1)
        if predicate and Begin_To_End_Tuple not in Begin_TO_End_Of_Predicate_List:
            # 将已经配对好的谓语结构的起始和终止存储在Begin_To_End_Of_Predicate_List里
            Begin_TO_End_Of_Predicate_List.append(Begin_To_End_Tuple)
            # 当前优先级及以上优先级能找到的谓语结构
            Priority_Now_And_Over_Predicate_List.append(predicate)
            # 最终句子的谓语结构（list里面的元素为字典{‘CONJn":'...',   'CONJ1’：'...' ,  '主句的谓语结构'：’...‘}）
            my_dict = {}
            my_dict['Predicate_Of_Main：'] = predicate
            Result_Predicate_List.append(my_dict)
            Singal_Main= True
            break
        else:
            continue

    if not Singal_Main:
        # 优先级二
        for i in range(len(splited_sentence)):
            # 在当前位置i
            # 在当前位置i前面是‘to’或'To'
            if i - 1 >= 0 and splited_sentence[i - 1] in ['to', 'To']:
                continue
            predicate_two_one = check_priority_two_one(splited_sentence, i)
            predicate_two_two = check_priority_two_two(splited_sentence, i)
            Predicate_Priority_Two_List = []
            Predicate_Priority_Two_List.append(predicate_two_one)
            Predicate_Priority_Two_List.append(predicate_two_two)
            predicate = max(Predicate_Priority_Two_List, key=len)
            # 如果优先级二所抓取到的谓语结构不为空且不在Begin_TO_End_Of_Predicate_List里
            Begin_To_End_Tuple = (i, i + len(predicate) - 1)
            if predicate and Begin_To_End_Tuple not in Begin_TO_End_Of_Predicate_List:
                # 将已经配对好的谓语结构的起始和终止存储在Begin_To_End_Of_Predicate_List里
                Begin_TO_End_Of_Predicate_List.append(Begin_To_End_Tuple)
                # 当前优先级及以上优先级能找到的谓语结构
                Priority_Now_And_Over_Predicate_List.append(predicate)
                # 最终句子的谓语结构（list里面的元素为字典{‘CONJn":'...',   'CONJ1’：'...' ,  '主句的谓语结构'：’...‘}）
                my_dict = {}
                my_dict['Predicate_Of_Main'] = predicate
                Result_Predicate_List.append(my_dict)
                Singal_Main= True
                break
            else:
                continue

    if not Singal_Main:
        # 3)按照优先级三抓取谓语结构
        # -----------------------------------------------------------------------
        for i in range(len(splited_sentence)):
            # 优先级三
            # 在当前位置i
            # 在当前位置i前面是‘to’或'To'
            if i - 1 >= 0 and splited_sentence[i - 1] in ['to', 'To']:
                continue
            predicate_three_one = check_priority_three_one(splited_sentence, i)
            predicate_three_two = check_priority_three_two(splited_sentence, i)
            Predicate_Priority_Three_List = []
            Predicate_Priority_Three_List.append(predicate_three_one)
            Predicate_Priority_Three_List.append(predicate_three_two)
            predicate = max(Predicate_Priority_Three_List, key=len)
            # 如果优先级二所抓取到的谓语结构不为空且不在Begin_TO_End_Of_Predicate_List里
            Begin_To_End_Tuple = (i, i + len(predicate) - 1)
            if predicate and Begin_To_End_Tuple not in Begin_TO_End_Of_Predicate_List:
                # 将已经配对好的谓语结构的起始和终止存储在Begin_To_End_Of_Predicate_List里
                Begin_TO_End_Of_Predicate_List.append(Begin_To_End_Tuple)
                # 当前优先级及以上优先级能找到的谓语结构
                Priority_Now_And_Over_Predicate_List.append(predicate)
                # 最终句子的谓语结构（list里面的元素为字典{‘CONJn":'...',   'CONJ1’：'...' ,  '主句的谓语结构'：’...‘}）
                my_dict = {}
                my_dict['Predicate_Of_Main'] = predicate
                Result_Predicate_List.append(my_dict)
                Singal_Main = True
                break
            else:
                continue

    if not Singal_Main:
        # （4）按照优先级四抓取谓语结构
        # -----------------------------------------------------------------------
        for i in range(len(splited_sentence)):
            # 优先级四
            # 在当前位置i
            # 在当前位置i前面是‘to’或'To'
            if i - 1 >= 0 and splited_sentence[i - 1] in ['to', 'To']:
                continue
            predicate_four_one = check_priority_four_one(splited_sentence, i)
            Predicate_Priority_Four_List = []
            # 如果优先级二所抓取到的谓语结构不为空且不在Begin_TO_End_Of_Predicate_List里
            Begin_To_End_Tuple = (i, i + len(predicate) - 1)
            if predicate and Begin_To_End_Tuple not in Begin_TO_End_Of_Predicate_List:
                # 将已经配对好的谓语结构的起始和终止存储在Begin_To_End_Of_Predicate_List里
                Begin_TO_End_Of_Predicate_List.append(Begin_To_End_Tuple)
                # 当前优先级及以上优先级能找到的谓语结构
                Priority_Now_And_Over_Predicate_List.append(predicate)
                # 最终句子的谓语结构（list里面的元素为字典{‘CONJn":'...',   'CONJ1’：'...' ,  '主句的谓语结构'：’...‘}）
                my_dict = {}
                my_dict['Predicate_Of_Main'] = predicate
                Result_Predicate_List.append(my_dict)
                Singal_Main= True
                break
            else:
                continue

    if  Singal_Main:
        print("-----------------------主句的谓语结构抓取OK-----------------------")
    else:
        my_dict={}
        my_dict['Predicate_Of_Main'] = None
        Result_Predicate_List.append(my_dict)
        print("-----------------------主句的谓语结构抓取ERROR-----------------------")
    # print(CONJ_List,CONJ_Location_List,CONJ_And_Location_Of_CONJ_List,Begin_TO_End_Of_Predicate_List)
    return Result_Predicate_List


if __name__ == '__main__':
    # sentence = "were known in children's growth."
    # splited_sentence =split_sentence_to_list.splited_sentence(sentence)
    # for i in range(len(splited_sentence)):
    #     the_predicate=check_priority_one_three(splited_sentence, i)
    #     if the_predicate:
    #         break
    # print(the_predicate)


    with open('example.txt', 'r') as file:
        sentences = [split_sentence_to_list.splited_sentence(line.strip()) for line in file]
    #逐行抓取lines里面每一个line的
    for sentence in sentences:
        Result_Predicate_List=extract_predicate(sentence)
        # print(CONJ_List,CONJ_Location_List,CONJ_And_Location_Of_CONJ_List,)
        with open('result.txt', 'a',encoding='utf-8') as file:
            file.write(str(Result_Predicate_List) + '\n')
        CONJ_List.clear()
        CONJ_Location_List.clear()
        CONJ_And_Location_Of_CONJ_List.clear()
        Begin_TO_End_Of_Predicate_List.clear()
        Result_Predicate_List.clear()