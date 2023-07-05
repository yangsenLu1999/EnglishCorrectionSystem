import mydb
import split_sentence_to_list

# #引入指示代词列表
# #指示代词
# demon_pron=['this', 'that', 'these', 'those']
#判断该单词是否是一个普通关联词 direct_conj
def is_a_direct_conj_or_not(splited_sentence :list,i :int)->bool:
    # because 关联词
    if splited_sentence[i] == "because":
        if i + 1 < len(splited_sentence) and splited_sentence[i + 1] == 'of':
            return False
        else:
            if i + 1 < len(splited_sentence) and splited_sentence[i + 1] != 'of':
                return True
    # 普通连接词
    one_word_direct_conj_list = ['what', 'how', 'why', 'where', 'when', 'who', 'whom', 'whose', 'which',
                                 'What', 'How', 'Why', 'Where', 'When', 'Who', 'Whom', 'Whose', 'Which',
                                 'whatever', 'wherever','whenever', 'whoever', 'whomever', 'whichever',
                                 'Whatever', 'Wherever', 'Whenever', 'Whoever', 'Whomever', 'Whichever',
                                 'whether', 'while', 'whilst',
                                 'Whether', 'While', 'Whilst',
                                 'although', 'though', 'lest','if',
                                 'Although','Though','Lest','If']
    if splited_sentence[i] in one_word_direct_conj_list:
        return True

    # #as关联词
    # if splited_sentence[i] =='as':
    #     if i+1<len(splited_sentence) and splited_sentence[i+1] =='if':
    #         return True
    #     if i+1<len(splited_sentence) and splited_sentence[i+1]!= 'though':
    #         return True

#定义单词once/so的从关判断 rule3
def once_so_rule3(splited_sentence :list,i :int)->str:
    #i+adj+n
    if i+2<len(splited_sentence) and mydb.id_apple_moun(splited_sentence[i+2])>=0:
        return "CONJ"
    #i+n+doing  ?????????忽略了多性动词在此处不起动词词性的情况
    elif i+2<len(splited_sentence) and mydb.id_apple_moun(splited_sentence[i+1])>=0 \
        and ( mydb.id_apple_verbpluspos_vbg_vsimple(splited_sentence[i+2])>=0 or mydb.id_apple_verbpluspos_double_vbg_vsimple_or_not(splited_sentence[i+2])):
        return "CONJ"
    else:
        return "ADV"

#定义单词once/so的从关判断 rule4
def once_so_rule4(splited_sentence :list,i :int)->str:
    #4.3
    #i+adv+to+vsimple
    if i+3<len(splited_sentence) and mydb.id_apple_adverb_word(splited_sentence[i+1])>=0 and splited_sentence[i+2] =="to" \
            and mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+3])>=0:
        return "CONJ"
    #i+adv+to+vcomplex
    elif i+3 < len(splited_sentence) and mydb.id_apple_adverb_word(splited_sentence[i+1])>= 0 and splited_sentence[i+2] == "to" \
            and mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i+ 3]) >= 0:
        return "CONJ"

    #4.4
    #i+adv+doing/done
    elif i+2<len(splited_sentence) and (mydb.id_vbg_vsimple_or_vbg_vcomplex(splited_sentence[i+2])>=0 or mydb.id_vbn_vsimple_or_vbn_vcomplex(splited_sentence[i+2])):
        if i+3< len(splited_sentence) and mydb.id_apple_moun(splited_sentence[i+3])>=0 :
            return "CONJ"
        else:
            return "ADV"

    #4.5
    #i+adv+从关  return True
    #普通从关
    elif i+2<len(splited_sentence) and is_a_direct_conj_or_not(splited_sentence,i+2):
        return "CONJ"
    #特殊从关
    elif i+2<len(splited_sentence) and is_a_indirect_conj_or_not(splited_sentence,i+2):
        return "CONJ"

    #4.6
    #i+adv+prep  return False
    elif i+2<len(splited_sentence) and mydb.id_apple_pronoun_word(splited_sentence[i+2])>=0:
        return "ADV"

    #4.1,4.2
    #i+（adv){0,}+(adj){0,}+n   once_so_rule3
    else:
        if i+2<len(splited_sentence):
            location=-1
            for x in range(i+2,len(splited_sentence)):
                if mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative(splited_sentence[x]):
                    continue
                elif mydb.id_apple_adjective_word_or_comparative_without_more_or_superlative(splited_sentence[x]):
                    location=x-1
            return once_so_rule3(splited_sentence,location)



#判断该单词once/so是否是一个特殊关联词 indirect_conj
def syntactic_role_of_the_once_so(splited_sentence :list ,i :int)->str:
    #once so的从关判断
    if splited_sentence[i] in ['once','so','Once','So']:
        #特别说明： so + V.    so 是从关 （so 的倒装句）
        if i+1<len(splited_sentence) and splited_sentence[i+1] in ['do','does','did']:
            return "CONJ"
        elif  i+1<len(splited_sentence) and splited_sentence[i+1] in ['am','is','are','was','were']:
            return "CONJ"
        #i-1是指示代词
        elif i-1>=0 and splited_sentence[i-1] in['this', 'that', 'these', 'those','This','That','These','Those']:
            return "ADV"
        #i-1是冠词
        elif i-1>=0 and splited_sentence[i-1] in ['a','an','the','A','An','The']:
            return "ADV"
        else:
            #1.+冠词 or 指示代词， then 是从关
            if i+1<len(splited_sentence) and splited_sentence[i+1] in ['a','an','the']:
                return "CONJ"
            elif i+1<len(splited_sentence) and splited_sentence[i+1] in['this', 'that', 'these', 'those']:
                return "CONJ"
            #2.+ n.   , then  是从关
            elif i+1<len(splited_sentence) and mydb.id_apple_moun(splited_sentence[i+1])>=0:
                return "CONJ"

            # 3.+adj.  向后遍历一位 ，    if :  +n.   then 是从关
			# 									elif: +doing   then 是从关
			# 									else: then 是副词
            elif i+1<len(splited_sentence) and ( mydb.id_apple_adjective_word(splited_sentence[i+1])>=0 \
                    or mydb.id_apple_adjective_comparative_without_more(splited_sentence[i+1])>=0 \
                    or mydb.id_apple_adjective_superlative_without_most(splited_sentence[i+1])>=0 ):
                return once_so_rule3(splited_sentence,i)

            # 4. + adv
            #判断是否符合规则四
            elif i+1<len(splited_sentence) and (mydb.id_apple_adverb_word(splited_sentence[i+1])>=0 \
                    or mydb.id_apple_adverb_comparative_without_more(splited_sentence[i+1])>=0 \
                    or mydb.id_apple_adverb_superlative_without_most(splited_sentence[i+1])>=0 ):
                return once_so_rule4(splited_sentence,i)

            #5. +to do ， 之后无逗号 then 从关
                        # 之后有逗号， then 副词
            elif i+3<len(splited_sentence) and splited_sentence[i+1]+" "+splited_sentence[i+2] == "to do":
                if splited_sentence[i+3]==',':
                    return "ADV"
                else:
                    return "CONJ"

            #6. +doing/done
            #单性动词的现在分词
            elif i+1<len(splited_sentence) and mydb.id_apple_verbpluspos_vbg_vsimple(splited_sentence[i+1])>=0:
                if i+2<len(splited_sentence) and mydb.id_apple_moun(splited_sentence[i+2])>=0:
                    return "CONJ"
                else:
                    return "ADV"
            #单性动词的过去分词
            elif i+1<len(splited_sentence) and mydb.id_apple_verbpluspos_vbn_vsimple(splited_sentence[i+1])>=0:
                if i+2<len(splited_sentence) and mydb.id_apple_moun(splited_sentence[i+2])>=0:
                    return "CONJ"
                else:
                    return "ADV"
            #多性动词的现在分词
            elif i+1<len(splited_sentence) and mydb.id_apple_verbpluspos_double_vbg_vcomplex(splited_sentence[i+1])>=0:
                if i+2<len(splited_sentence) and mydb.id_apple_moun(splited_sentence[i+2])>=0:
                    return "CONJ"
                else:
                    return "ADV"
            #多性动词的过去分词
            elif i+1<len(splited_sentence) and mydb.id_apple_verbpluspos_double_vbn_vcomplex(splited_sentence[i+1])>=0:
                if i+2<len(splited_sentence) and mydb.id_apple_moun(splited_sentence[i+2])>=0:
                    return "CONJ"
                else:
                    return "ADV"

            #7 +从关 return True
            elif i+1<len(splited_sentence) and is_a_conj_or_not(splited_sentence,i+1):
                return "CONJ"

            #8 +prep return False
            elif i+1<len(splited_sentence) and mydb.id_apple_pronoun_word(splited_sentence[i+1])>=0:
                return "ADV"
            else:#??????????????????????????????都不满足，怎么办？
                return "UNKNOWN"

#定义as/than的从关判断规则1
def as_than_rule1(splited_sentence:list,i:int)->str:
    # 向后遍历
    for index in range(i + 2, len(splited_sentence)):
        if mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[index])>=0:
            continue
        elif mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[index])>=0 or mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[index])>=0:
            return "CONJ"
        else:
            return "PREP"

#定义as/than的从关判断规则2
def as_than_rule2(splited_sentence:list,i:int)->str:
    if i+2<len(splited_sentence) and mydb.id_apple_moun(splited_sentence[i+2])>=0:
        return as_than_rule1(splited_sentence,i+1)

#定义as/than的从关判断规则3
def as_than_rule3(splited_sentence:list,i:int)->str:
    if i+2<len(splited_sentence) and mydb.id_apple_moun(splited_sentence[i+2]):
        return "CONJ"
    elif i+2<len(splited_sentence) and mydb.id_apple_adjective_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+2]) :
        #?????????????????????????????
        return as_than_rule2(splited_sentence,i+1)
    else:
        #????????????????????????????
        if i+2<len(splited_sentence) and mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+2]) :
            if i+3<len(splited_sentence) and mydb.id_apple_adjective_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+3]):
                return as_than_rule3(splited_sentence,i+2)
            else:
                return "ADV"

#定义as/than的从关判断规则4
def as_than_rule4(splited_sentance:list,i:int)->str:
    #?????????????????????????????????????
    if  i+3<len(splited_sentance) and mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+3])>=0:
        return "CONJ"
    else:
        return "ADV"

#定义as/than的从关判断规则5
def as_than_rule5(splited_sentence:list,i:int)->str:
    if i+2<len(splited_sentence) and mydb.id_apple_moun(splited_sentence[i+2])>=0:
        return as_than_rule1(splited_sentence,i+1)
    else:
        return "ADV"
#
# # #定义as/than的从关判断规则6
# # def as_than_rule6(splited_sentence:list,i:int)->str:
# #     pass

#单词as/than的从关判断
def syntactic_role_of_the_as_than(splited_sentence:list,i:int)->str:
    if splited_sentence[i] in ['as','than']:
        # as关联词
        if splited_sentence[i] == 'as':
            if i + 1 < len(splited_sentence) and splited_sentence[i + 1] == 'if':
                return True
            if i + 1 < len(splited_sentence) and splited_sentence[i + 1] == 'though':
                return True
        #rule1
        elif i + 1 < len(splited_sentence):
            # 1
            if splited_sentence[i + 1] in ['a', 'an', 'the'] or splited_sentence[i + 1] in ["this","that","these","those"] or mydb.id_apple_moun(splited_sentence[i+ 1]) >= 0:
                if i + 2 < len(splited_sentence):
                    return as_than_rule1(splited_sentence, i)
                else:
                    return "PREP"
        #rule2
        elif i+1<len(splited_sentence) and mydb.id_apple_adjective_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+1])>=0:
            return as_than_rule2(splited_sentence, i)

        #rule3
        elif i+1<len(splited_sentence) and mydb.id_apple_adjective_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+1])>=0:
            return as_than_rule3(splited_sentence, i)

        #rule4
        elif i+1<len(splited_sentence) and i+2 < len(splited_sentence) and splited_sentence[i+1]=="to" and splited_sentence[i+2]=="do":
            return as_than_rule4(splited_sentence, i)

        #rule5
        elif i+1<len(splited_sentence):
            if (splited_sentence[i+1]):
                return as_than_rule5(splited_sentence,i)
            ####????????????????????????忽略多性动词的情况
            # elif ex_predicate.search_in_label_vcomplex_the_word_is_vbg_vcomplex_or_not(splited_sentence[i+1]):
            #     return as_than_rule5(splited_sentence,i)

        #rule6:
        #??????????????????????????????????????????
        elif i+1<len(splited_sentence) and mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+1])>=0:
            return "CONJ"

        #rule7:
        elif i+1<len(splited_sentence) :
            if is_a_conj_or_not(splited_sentence[i+1]):
                if splited_sentence[i+1] in ['who','what','which','whome']:
                    if i+2<len(splited_sentence) and ( mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+2])>=0 or mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i+2])>=0):
                        if i+3<len(splited_sentence) and ( mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+2])>=0 or mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i+2])>=0):
                            return "CONJ"
                        else:
                            return "PREP"
                else:
                    return "CONJ"

        #rule8:
        elif i+1<len(splited_sentence) and mydb.id_apple_prep(splited_sentence[i+1])>=0:
            return "CONJ"

#单词for/until/till/before/after/since的从关判断rule1
def for_until_till_before_after_since_rule1(splited_sentence:list,i:int)->str:
    return "CONJ"

#单词for/until/till/before/after/since的从关判断rule2
def for_until_till_before_after_since_rule2(splited_sentence:list,i:int)->str:
    return "CONJ"

#单词for/until/till/before/after/since的从关判断rule3
def for_until_till_before_after_since_rule3(splited_sentence:list,i:int)->str:
    if i+4<len(splited_sentence) and is_a_conj_or_not(splited_sentence[i+4]):
        return "PREP"
    #N/A 是什么？？？？？？？？？？？？？？？？？？？？？？？？
    #3.+adv.+ adj. +n.    if +关联词 or +N/A, then for 是介词
                        # elif 后遍历到谓语动词，并且中间无关联词， then for 是从关
    elif i+4>len(splited_sentence)-1 :
        return "PREP"
    else:
        pass

#单词for/until/till/before/after/since的从关判断rule4
def for_until_till_before_after_since_rule4(splited_sentence:list,i:int)->str:
    return "CONJ"

#单词for/until/till/before/after/since的从关判断rule5
def for_until_till_before_after_since_rule5(splited_sentence:list,i:int)->str:
    if i+1<len(splited_sentence) and is_a_conj_or_not(splited_sentence,i+1):
        return "PREP"
    elif i+1>=len(splited_sentence)-1:
        return "PREP"
    else:
        for x in range(i+1,len(splited_sentence)):
            if is_a_conj_or_not(splited_sentence,x):
                break
            # elif expredicate.ex_predicate(splited_sentence,x):
            #     return "CONJ"
            else:
                continue
        return "PREP"

#单词for/until/till/before/after/since从关判断
def syntactic_role_of_the_for_until_till_before_after_since(splited_sentence:list,i:int)->str:
    if splited_sentence[i] in ['for','until','till','before','after','since','Since']:
        #since的特殊处理
        if splited_sentence[i] in ["since" ,"Since"]:
            if i+1<len(splited_sentence) and splited_sentence[i+1]==",":
                return "ADV"
            elif i+1<len(splited_sentence) and splited_sentence[i+1]==".":
                return "ADV"
            else:
                if i+1<len(splited_sentence) and mydb.id_apple_pronoun_word(splited_sentence[i+1])>=0:
                    return "PREP"
                else:
                    return "CONJ"
        elif i+1<len(splited_sentence) and splited_sentence[i+1] in ['me','them','him']:
            return "PREP"
        #rule1
        elif i+1<len(splited_sentence) and mydb.id_apple_prep(splited_sentence[i+1])>=0:
            return "CONJ"
        #rule2
        elif i+2<len(splited_sentence) and splited_sentence[i+1]=="to" and (mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+2])>=0 or mydb.id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[i+2])>=0):
            return "CONJ"
        #rule3
        elif i+3<len(splited_sentence) and mydb.id_apple_adverb_word(splited_sentence[i+1])>=0 and mydb.id_apple_adverb_word(splited_sentence[i+2])>=0 and mydb.id_apple_mount_word(splited_sentence[i+3])>=0:
            return for_until_till_before_after_since_rule3(splited_sentence,i)
        #rule4
        # elif i+2<len(splited_sentence) and mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+2])>=0  and (mydb.id_apple_moun(splited_sentence[i+2])>=0 or mydb.is_vbg_vsimple_or_vbg_vcomplex(splited_sentence[i+2] >=0):
        #     return for_until_till_before_after_since_rule4(splited_sentence,i)
        # elif i+2<len(splited_sentence) and mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+2])>=0 and ( splited_sentence[i+1]=="to" and mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i+2])>=0):
        #     return for_until_till_before_after_since_rule4(splited_sentence,i)
        #rule5
        else:
            if i+1<len(splited_sentence) and (mydb.id_vbg_vsimple_or_vbg_vcomplex(splited_sentence[i+1])>=0 or mydb.id_apple_moun(splited_sentence[i+1])>=0):
                return for_until_till_before_after_since_rule5(splited_sentence,i)

#单词whereas/however的从关判断
def syntactic_role_of_the_whereas_however(splited_sentence:list,i:int)->str:
    if splited_sentence[i] in ['whereas','however']:
        if i+1<len(splited_sentence) and splited_sentence[i+1]=="," :
            return "ADV"
        else:
            return "UNKNOWN"


#单词that的从关判断  4种词性： 代词 PRONOUN、指示代词DEMON_PRON、从关CONJ、副词ADV
def syntactic_role_of_the_that(splited_sentence:list,i:int)->str:

    if splited_sentence[i] in ['that','That']:
        #rule1 That+that
        if i+1<len(splited_sentence) and splited_sentence[i+1]==["that"]:
            #PREP
            if i-1>=0 and mydb.id_apple_prep(splited_sentence[i-1])>=0:
                return "PRONOUN"
            #to do
            elif i-2>=0 and splited_sentence[i-2]=="to" and (mydb.id_apple_verbpluspos_vori_vsimple(splited_sentence[i-2])>=0 or mydb.id_apple_verbpluspos_vori_vcomplex(splited_sentence[i-2])>=0):
                return "PRONOUN"
            #doing
            elif i-1>=0 and mydb.is_vbg_vsimple_or_vbg_vcomplex(splited_sentence[i-1])>=0:
                return  "PRONOUN"
        elif i+1<len(splited_sentence) and splited_sentence[i+1]=="," :
            return "CONJ"
        #rule2
        #2.That + 冠词： 从关
        elif i+1<len(splited_sentence) and splited_sentence[i+1] in ["a","an", "the"]:
            return "CONJ"
        #rule3
        #3.That + 代词: 从关
        elif i+1<len(splited_sentence) and mydb.id_apple_pronoun_word(splited_sentence[i+1])>=0:
            return "CONJ"
        #there 作代词
        elif i+1<len(splited_sentence) and splited_sentence[i+1]=="there":
            return "CONJ"
        #后跟情态动词
        elif i+1<len(splited_sentence) and splited_sentence[i+1]=="may":
            return "CONJ"

        #that后跟一个is am are
        elif i+1<len(splited_sentence) and splited_sentence[i+1]=="is":
            return "DEMON_PRON"
        # #that后紧跟一个名词单数
        # elif i+1<len(splited_sentence) and mydb.id_apple_moun_word(splited_sentence[i+1])>=0:
        #     return "DEMON_PRON"

        #rule5
        elif i+1<len(splited_sentence) and mydb.id_apple_moun(splited_sentence[i+1])>=0:
            #rule5 a
            if mydb.id_apple_moun_noun_plural(splited_sentence[i+1])>=0:
                return "CONJ"
            #rule5 b
            else:
                #rule5 b（i）
                if i-1>=0 and mydb.id_apple_prep(splited_sentence[i-1])>=0:
                    return "DEMON_PRON"
                if i - 1 >= 0 and is_a_conj_or_not(splited_sentence, i - 1):
                    return "DEMON_PRON"
                #rule5 b(ii)
                elif i-1==0 or splited_sentence[i-1] =="," :
                    #rule5 b(ii) a)
                    #??????????
                    pass
                #rule5 b(iii)
                #?????????????
                else:
                    pass
        elif i+1<len(splited_sentence) and splited_sentence[i+1]=="deserve":
            return "CONJ"
        #rule6
        elif i+1<len(splited_sentence) and mydb.id_apple_adjective_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+1])>=0:
            if i+1<len(splited_sentence) and mydb.id_apple_moun(splited_sentence[i+1])>=0:
                pass
                #???????????
        #rule7
        elif i+1<len(splited_sentence) and mydb.id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[i+1])>=0:
            pass
        #rule8
        else:
            return "UNKNOWN"


#判断单词是否是特殊从关   ???????????????????
def is_a_indirect_conj_or_not(splited_sentence:list,i:int)->bool:
    if syntactic_role_of_the_once_so(splited_sentence,i)=="CONJ" or syntactic_role_of_the_as_than(splited_sentence,i) =="CONJ"\
            or syntactic_role_of_the_for_until_till_before_after_since(splited_sentence,i)=="CONJ" or syntactic_role_of_the_whereas_however(splited_sentence,i)=="CONJ"\
        or syntactic_role_of_the_that(splited_sentence,i)=="CONJ":
        return True
    else:
        return False

#判断句子中是否有从关（including direct_conj and indirect_conj）
def is_a_conj_or_not(splited_sentence:list,i:int)->bool:
    if is_a_direct_conj_or_not(splited_sentence,i) or is_a_indirect_conj_or_not(splited_sentence,i):
        return True
    else:
        return False



if __name__ == '__main__':
    lines_list = []
    splited_sentences_list=[]
    count=1
    with open('test.txt', 'r') as file:
        for line in file:
            lines_list.append(line.strip())
    for i in range(len(lines_list)):
        splited_sentences_list.append(split_sentence_to_list.splited_sentence(lines_list[i]))
    # print(splited_sentences_list)
    for splited_sentence in splited_sentences_list:
        # print(i)
        conj=[]
        print("当前到了第" + str(count) + "个句子")
        for i in range(len(splited_sentence)):
            if is_a_conj_or_not(splited_sentence,i):
                conj.append(splited_sentence[i])
            # print("当前处理到了第{}个单词".format(i))
        print(conj)
        count=count+1








