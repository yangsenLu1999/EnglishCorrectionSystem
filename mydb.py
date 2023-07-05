import re

#连接数据库
import mysql.connector

# 连接数据库
mydb =mysql.connector.connect(user='root', password='1234',
                              host='192.168.100.120', database='tencent')
mycursor = mydb.cursor()

#动词原型vori 三单vbz 过去式vbd 过去分词vbn 现在分词vbg

#把数据库数据加载到本地：
#
#使用python读取mysql中的数据表apple_verbpluspos，将word列的数据当作字典的key，
# 而id、pos、_pos、vbz、vbg、vbd、vbn当作索引值，整体类似与josn格式
#读取数据库表单性动词表apple_verbpluspos
def read_apple_verbpluspos(dictionary_of_apple_verbpluspos):
    sql="SELECT id, word, pos, _pos, vbz, vbg, vbd, vbn FROM apple_verbpluspos"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for row in result:
        dictionary_of_apple_verbpluspos[row[1]] = {
            "wordid": row[0],
            "pos": row[2],
            "_pos": row[3],
            "vbz": row[4],
            "vbg": row[5],
            "vbd": row[6],
            "vbn": row[7]
        }
    # 返回字典对象
    return dictionary_of_apple_verbpluspos

# dictionary_of_apple_verbpluspos_empty={}
# dictionary_of_apple_verbpluspos = read_apple_verbpluspos(dictionary_of_apple_verbpluspos_empty)
# print(dictionary_of_apple_verbpluspos)

#读取数据库多性动词表apple_verbpluspos_double
#以word为key，id、pos、_pos、vbz、vbg、vbd、vbn为索引值，整体类似与josn格式
def read_apple_verbpluspos_double(dictionary_of_apple_verbpluspos_double):
    sql="SELECT word, id, pos, _pos, vbz, vbg, vbd, vbn FROM apple_verbpluspos_double"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for row in result:
        dictionary_of_apple_verbpluspos_double[row[0]] = {
            "wordid": row[1],
            "pos": row[2],
            "_pos": row[3],
            "vbz": row[4],
            "vbg": row[5],
            "vbd": row[6],
            "vbn": row[7]
        }
    # 返回字典对象
    return dictionary_of_apple_verbpluspos_double

#读取动词组合表
#以text为key，id、vbz、vbg、vbd、vbn为索引值，整体类似与josn格式
def read_apple_fixedmatch(dictionary_of_apple_fixedmatch):
    sql="SELECT text, id, vbz, vbg, vbd, vbn FROM apple_fixedmatch"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for row in result:
        dictionary_of_apple_fixedmatch[row[0]] = {
            "wordid": row[1],
            "vbz": row[2],
            "vbg": row[3],
            "vbd": row[4],
            "vbn": row[5]
        }
    # 返回字典对象
    return dictionary_of_apple_fixedmatch

#读取名词表apple_moun
#以word为key，id、words、pos为索引值，整体类似与josn格式
def read_apple_moun(dictionary_of_apple_moun):
    sql="SELECT word, id, words, pos FROM apple_moun"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for row in result:
        dictionary_of_apple_moun[row[0]] = {
            "wordid": row[1],
            "words": row[2],
            "pos": row[3]
        }
    # 返回字典对象
    return dictionary_of_apple_moun

#读取形容词表apple_adjective
#以word为key，id、pos、comparative、superlative为索引值，整体类似与josn格式
def read_apple_adjective(dictionary_of_apple_adjective):
    sql="SELECT word, id, pos, comparative, superlative FROM apple_adjective"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for row in result:
        dictionary_of_apple_adjective[row[0]] = {
            "wordid": row[1],
            "pos": row[2],
            "comparative": row[3],
            "superlative": row[4]
        }
    # 返回字典对象
    return dictionary_of_apple_adjective

#读取副词表apple_adverb
#以word为key，id、pos、comparative、superlative为索引值，整体类似与josn格式
def read_apple_adverb(dictionary_of_apple_adverb):
    sql="SELECT word, id, pos, comparative, superlative FROM apple_adverb"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for row in result:
        dictionary_of_apple_adverb[row[0]] = {
            "wordid": row[1],
            "pos": row[2],
            "comparative": row[3],
            "superlative": row[4]
        }
    # 返回字典对象
    return dictionary_of_apple_adverb

#读取介词表apple_prep
#以word为key，id、pos为索引值，整体类似与josn格式
def read_apple_prep(dictionary_of_apple_prep):
    sql="SELECT word, id, pos FROM apple_prep"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for row in result:
        dictionary_of_apple_prep[row[0]] = {
            "wordid": row[1],
            "pos": row[2]
        }
    # 返回字典对象
    return dictionary_of_apple_prep

#读取代词表apple_pronoun
#以word为key，id、pos、type为索引值，整体类似与josn格式
def read_apple_pronoun(dictionary_of_apple_pronoun):
    sql="SELECT word, id, pos, type FROM apple_pronoun"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for row in result:
        dictionary_of_apple_pronoun[row[0]] = {
            "wordid": row[1],
            "pos": row[2],
            "type": row[3]
        }
    # 返回字典对象
    return dictionary_of_apple_pronoun

#读取量词表apple_quantifierlemma
#以word为key，id为索引值，整体类似与josn格式
def read_apple_quantifierlemma(dictionary_of_apple_quantifierlemma):
    sql="SELECT word, id FROM apple_quantifierlemma"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for row in result:
        dictionary_of_apple_quantifierlemma[row[0]] = {
            "wordid": row[1]
        }
    # 返回字典对象
    return dictionary_of_apple_quantifierlemma

#读取非动词表apple_nonverbpos
#以word为key，id、pos为索引值，整体类似与josn格式
def read_apple_nonverbpos(dictionary_of_apple_nonverbpos):
    sql="SELECT word, id, pos FROM apple_nonverbpos"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for row in result:
        dictionary_of_apple_nonverbpos[row[0]] = {
            "wordid": row[1],
            "pos": row[2]
        }
    # 返回字典对象
    return dictionary_of_apple_nonverbpos

#单性动词表
dictionary_of_apple_verbpluspos_empty={}
dictionary_of_apple_verbpluspos = read_apple_verbpluspos(dictionary_of_apple_verbpluspos_empty)
# print(dictionary_of_apple_verbpluspos)

#多性动词表
dictionary_of_apple_verbpluspos_double_empty={}
dictionary_of_apple_verbpluspos_double = read_apple_verbpluspos_double(dictionary_of_apple_verbpluspos_double_empty)
# print(dictionary_of_apple_verbpluspos_double)

#动词组合表
dictionary_of_apple_fixedmatch_empty={}
dictionary_of_apple_fixedmatch = read_apple_fixedmatch(dictionary_of_apple_fixedmatch_empty)
# print(dictionary_of_apple_fixedmatch)

#名词表
dictionary_of_apple_moun_empty={}
dictionary_of_apple_moun = read_apple_moun(dictionary_of_apple_moun_empty)
# print(dictionary_of_apple_moun)

#形容词表
dictionary_of_apple_adjective_empty={}
dictionary_of_apple_adjective = read_apple_adjective(dictionary_of_apple_adjective_empty)
# print(dictionary_of_apple_adjective)

#副词表
dictionary_of_apple_adverb_empty={}
dictionary_of_apple_adverb = read_apple_adverb(dictionary_of_apple_adverb_empty)
# print(dictionary_of_apple_adverb)

#介词表
dictionary_of_apple_prep_empty={}
dictionary_of_apple_prep = read_apple_prep(dictionary_of_apple_prep_empty)

#代词表
dictionary_of_apple_pronoun_empty={}
dictionary_of_apple_pronoun = read_apple_pronoun(dictionary_of_apple_pronoun_empty)
# print(dictionary_of_apple_pronoun)

#量词表
dictionary_of_apple_quantifierlemma_empty={}
dictionary_of_apple_quantifierlemma = read_apple_quantifierlemma(dictionary_of_apple_quantifierlemma_empty)
# print(dictionary_of_apple_quantifierlemma)

#非动词表
dictionary_of_apple_nonverbpos_empty={}
dictionary_of_apple_nonverbpos = read_apple_nonverbpos(dictionary_of_apple_nonverbpos_empty)
# print(dictionary_of_apple_nonverbpos)



#检测一个单词是不是单性动词的原型vori_vsimple
def id_apple_verbpluspos_vori_vsimple(word:str):
    for i in dictionary_of_apple_verbpluspos:
        if i == word:
            return dictionary_of_apple_verbpluspos[i]["wordid"]
        else:
            continue
    return -1

# print(is_apple_verbpluspos_vori_vsimple_or_not("achieve"))

#检测一个单词是否是单性动词的三单vbz_vsimple
def id_apple_verbpluspos_vbz_vsimple(word:str)->int:
    for i in dictionary_of_apple_verbpluspos:
        if word == dictionary_of_apple_verbpluspos[i]["vbz"]:
            return dictionary_of_apple_verbpluspos[i]["wordid"]
        else:
            continue
    return -1
# print(is_apple_verbpluspos_vbz_simple_or_not("achieves"))

#检测一个单词是否是单性动词的现在分词vbg_vsimple
def id_apple_verbpluspos_vbg_vsimple(word:str)->int:
    for i in dictionary_of_apple_verbpluspos:
        if word == dictionary_of_apple_verbpluspos[i]["vbg"]:
            return dictionary_of_apple_verbpluspos[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是单性动词的过去式vbd_vsimple
def id_apple_verbpluspos_vbd_vsimple(word:str)->int:
    for i in dictionary_of_apple_verbpluspos:
        if word == dictionary_of_apple_verbpluspos[i]["vbd"]:
            return dictionary_of_apple_verbpluspos[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是单性动词的过去分词vbn_vsimple
def id_apple_verbpluspos_vbn_vsimple(word:str)->int:
    for i in dictionary_of_apple_verbpluspos:
        if word == dictionary_of_apple_verbpluspos[i]["vbn"]:
            return dictionary_of_apple_verbpluspos[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是多性动词的原型vori_vcomplex
def id_apple_verbpluspos_double_vori_vcomplex(word:str)->int:
    for i in dictionary_of_apple_verbpluspos_double:
        if word == i:
            return dictionary_of_apple_verbpluspos_double[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是多性动词的三单vbz_vcomplex
def id_apple_verbpluspos_double_vbz_vcomplex(word:str)->int:
    for i in dictionary_of_apple_verbpluspos_double:
        if word == dictionary_of_apple_verbpluspos_double[i]["vbz"]:
            return dictionary_of_apple_verbpluspos_double[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是多性动词的现在分词vbg_vcomplex
def id_apple_verbpluspos_double_vbg_vcomplex(word:str)->int:
    for i in dictionary_of_apple_verbpluspos_double:
        if word == dictionary_of_apple_verbpluspos_double[i]["vbg"]:
            return dictionary_of_apple_verbpluspos_double[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是多性动词的过去式vbd_vcomplex
def id_apple_verbpluspos_double_vbd_vcomplex(word:str)->int:
    for i in dictionary_of_apple_verbpluspos_double:
        if word == dictionary_of_apple_verbpluspos_double[i]["vbd"]:
            return dictionary_of_apple_verbpluspos_double[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是多性动词的过去分词vbn_vcomplex
def id_apple_verbpluspos_double_vbn_vcomplex(word:str)->int:
    for i in dictionary_of_apple_verbpluspos_double:
        if word == dictionary_of_apple_verbpluspos_double[i]["vbn"]:
            return dictionary_of_apple_verbpluspos_double[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是单性动词的现在分词或多性动词的现在分词
def id_vbg_vsimple_or_vbg_vcomplex(word:str)->int:
    for i in dictionary_of_apple_verbpluspos:
        if word==dictionary_of_apple_verbpluspos[i]["vbg"]:
            return dictionary_of_apple_verbpluspos[i]["wordid"]
        else:
            continue
    for i in dictionary_of_apple_verbpluspos_double:
        if word ==dictionary_of_apple_verbpluspos_double[i]["vbg"]:
            return dictionary_of_apple_verbpluspos_double[i]["wordid"]
        else:
            continue
    return -1


#检测一个单词是否是单性动词的过去分词或多性动词的过去分词
def id_vbn_vsimple_or_vbn_vcomplex(word:str)->int:
    for i in dictionary_of_apple_verbpluspos:
        if word==dictionary_of_apple_verbpluspos[i]["vbn"]:
            return dictionary_of_apple_verbpluspos[i]["wordid"]
        else:
            continue
    for i in dictionary_of_apple_verbpluspos_double:
        if word ==dictionary_of_apple_verbpluspos_double[i]["vbn"]:
            return dictionary_of_apple_verbpluspos_double[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是组成动词词组的原型
def id_apple_fixedmatch_text(splited_sentence:list,index:int):
    word_sentence = splited_sentence[index]+" "+splited_sentence[index+1]
    for i in dictionary_of_apple_fixedmatch:
        if word_sentence== i:
            return int(dictionary_of_apple_fixedmatch[i]["wordid"])
        else:
            continue
    return -1

#检测一个单词是否是组成动词词组的三单
def id_apple_fixedmatch_vbz(splited_sentence:list,index:int):
    word_sentence = splited_sentence[index]+" "+splited_sentence[index+1]
    for i in dictionary_of_apple_fixedmatch:
        if word_sentence==dictionary_of_apple_fixedmatch[i]["vbz"]:
            return int(dictionary_of_apple_fixedmatch[i]["wordid"])

        else:
            continue
    return -1

#检测一个单词是否是组成动词词组的现在分词
def id_apple_fixedmatch_vbg(splited_sentence:list,index:int):
    word_sentence = splited_sentence[index]+" "+splited_sentence[index+1]
    for i in dictionary_of_apple_fixedmatch:
        if word_sentence==dictionary_of_apple_fixedmatch[i]["vbg"]:
            return int(dictionary_of_apple_fixedmatch[i]["wordid"])
        else:
            continue
    return -1

#检测一个单词是否是组成动词词组的过去式
def id_apple_fixedmatch_vbd(splited_sentence:list,index:int):
    word_sentence = splited_sentence[index]+" "+splited_sentence[index+1]
    for i in dictionary_of_apple_fixedmatch:
        if word_sentence==dictionary_of_apple_fixedmatch[i]["vbd"]:
            return int(dictionary_of_apple_fixedmatch[i]["wordid"])

        else:
            continue
    return -1

#检测一个单词是否是组成动词词组的过去分词
def id_apple_fixedmatch_vbn(splited_sentence:list,index:int):
    word_sentence = splited_sentence[index]+" "+splited_sentence[index+1]
    for i in dictionary_of_apple_fixedmatch:
        if word_sentence==dictionary_of_apple_fixedmatch[i]["vbn"]:
            return int(dictionary_of_apple_fixedmatch[i]["wordid"])

        else:
            continue
    return -1

#检测一个单词是否是名词的单数
def id_apple_moun_noun_origin(word:str)->int:
    for i in dictionary_of_apple_moun:
        if word == i:
            return int(dictionary_of_apple_moun[i]["wordid"])
        else:
            continue
    return -1

#检测一个单词是否是名词的复数
def id_apple_moun_noun_plural(word:str)->int:
    for i in dictionary_of_apple_moun:
        if word == dictionary_of_apple_moun[i]["words"]:
            return int(dictionary_of_apple_moun[i]["wordid"])
        else:
            continue
    return -1

#检测一个单词是否是名词的单数或者复数
def id_apple_moun(word:str)->int:
    for i in dictionary_of_apple_moun:
        if word == i:
            return int(dictionary_of_apple_moun[i]["wordid"])
        elif word == dictionary_of_apple_moun[i]["words"]:
            return int(dictionary_of_apple_moun[i]["wordid"])
        else:
            continue
    return -1

#检测一个单词是否是形容词原型
def id_apple_adjective_word(word:str)->int:
    for i in dictionary_of_apple_adjective:
        # if word ==dictionary_of_apple_adjective[i]["word"]:
        if word ==i:
            return dictionary_of_apple_adjective[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是不带more的形容词比较级
def id_apple_adjective_comparative_without_more(word:str)->int:
    for i in dictionary_of_apple_adjective:
        if word ==dictionary_of_apple_adjective[i]["comparative"]:
            return dictionary_of_apple_adjective[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是带more的形容词比较级
def id_apple_adjective_comparative_with_more(splited_sentence:list,index:int)->int:
    words_sentence=splited_sentence[index-1]+" "+splited_sentence[index]
    for i in dictionary_of_apple_adjective:
        if words_sentence==dictionary_of_apple_adjective[i]["comparative"]:
            return  dictionary_of_apple_adjective[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是不带more的形容词最高级
def id_apple_adjective_superlative_without_most(word:str)->int:
    for i in dictionary_of_apple_adjective:
        if  word ==dictionary_of_apple_adjective[i]["superlative"]:
            return dictionary_of_apple_adjective[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是带more的形容词最高级
def id_apple_adjective_superlative_with_most(splited_sentence:list,index:int)->int:
    words_sentence=splited_sentence[index-1]+" "+splited_sentence[index]
    for i in dictionary_of_apple_adjective:
        if words_sentence==dictionary_of_apple_adjective[i]["superlative"]:
            return  dictionary_of_apple_adjective[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是形容词原型或不带more的形容词比较级或不带most的形容词最高级
def id_apple_adjective_word_or_comparative_without_more_or_superlative_without_most(word:str)->int:
    for i in dictionary_of_apple_adjective:
        if word ==i:
            return dictionary_of_apple_adjective[i]["wordid"]
        elif word ==dictionary_of_apple_adjective[i]["comparative"]:
            return dictionary_of_apple_adjective[i]["wordid"]
        elif word ==dictionary_of_apple_adjective[i]["superlative"]:
            return dictionary_of_apple_adjective[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是副词原型
def id_apple_adverb_word(word:str)->int:
    for i in dictionary_of_apple_adverb:
        if word ==i:
            return dictionary_of_apple_adverb[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是副词的不带more的比较级
def id_apple_adverb_comparative_without_more(word:str)->int:
    for i in dictionary_of_apple_adverb:
        if word ==dictionary_of_apple_adverb[i]["comparative"]:
            return dictionary_of_apple_adverb[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是副词的带more的比较级
def id_apple_adverb_comparative_with_more(splited_sentence:list,index:int)->int:
    words_sentence=splited_sentence[index-1]+" "+splited_sentence[index]
    for i in dictionary_of_apple_adverb:
        if words_sentence==dictionary_of_apple_adverb[i]["comparative"]:
            return  dictionary_of_apple_adverb[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是副词的不带most的最高级
def id_apple_adverb_superlative_without_most(word:str)->int:
    for i in dictionary_of_apple_adverb:
        if word ==dictionary_of_apple_adverb[i]["superlative"]:
            return dictionary_of_apple_adverb[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是副词的带most的最高级
def id_apple_adverb_superlative_with_most(splited_sentence:list,index:int)->int:
    words_sentence=splited_sentence[index-1]+" "+splited_sentence[index]
    for i in dictionary_of_apple_adverb:
        if words_sentence==dictionary_of_apple_adverb[i]["superlative"]:
            return  dictionary_of_apple_adverb[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是副词原型或不带more的比较级或不带most的最高级
def id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(word:str)->int:
    for i in dictionary_of_apple_adverb:
        if word ==i:
            return dictionary_of_apple_adverb[i]["wordid"]
        elif word ==dictionary_of_apple_adverb[i]["comparative"]:
            return dictionary_of_apple_adverb[i]["wordid"]
        elif word ==dictionary_of_apple_adverb[i]["superlative"]:
            return dictionary_of_apple_adverb[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是介词
def id_apple_prep(word:str)->int:
    for i in dictionary_of_apple_prep:
        if word ==i:
            return dictionary_of_apple_prep[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是代词
def id_apple_pronoun_word(word:str)->int:
    for i in dictionary_of_apple_pronoun:
        if word ==i:
            return dictionary_of_apple_pronoun[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是量词
def id_apple_quantifierlemma(word:str)->int:
    for i in dictionary_of_apple_quantifierlemma:
        if word ==i:
            return dictionary_of_apple_quantifierlemma[i]["wordid"]
        else:
            continue
    return -1

#检测一个单词是否是非动词
def id_apple_nonverbpos(word:str)->int:
    for i in dictionary_of_apple_nonverbpos:
        if word ==i:
            return dictionary_of_apple_nonverbpos[i]["wordid"]
        else:
            continue
    return -1

if __name__ == '__main__':
    # print(dictionary_of_apple_verbpluspos)

    print(id_apple_adjective_word("happy"),type(id_apple_adjective_word("happy")))
    #406 <class 'int'>

    splited_sentence = ['happier']
    print(id_apple_adjective_comparative_without_more(0),type(id_apple_adjective_comparative_without_more(0)))
    #-1 <class 'int'>

    splited_sentence = ['more','frequent']
    print(id_apple_adjective_comparative_with_more(splited_sentence,1),type(id_apple_adjective_comparative_with_more(splited_sentence,1)))
    #374 <class 'int'>

    splited_sentence = ['go','out']
    print(id_apple_fixedmatch_text(splited_sentence,0),type(id_apple_fixedmatch_text(splited_sentence,0)))
    #99 <class 'str'>

    splited_sentence = ['goes','out']
    print(id_apple_fixedmatch_vbz(splited_sentence,0),type(id_apple_fixedmatch_vbz(splited_sentence,0)))
    #99 <class 'str'>

    splited_sentence = ['carried', 'out']
    print(id_apple_fixedmatch_vbn(splited_sentence, 0), type(id_apple_fixedmatch_vbn(splited_sentence, 0)))
    # 49 <class 'str'>

    splited_sentence = ['carried', 'out']
    print(id_apple_fixedmatch_vbd(splited_sentence, 0), type(id_apple_fixedmatch_vbd(splited_sentence, 0)))
    # 49 <class 'str'>

    splited_sentence=['book']
    print(id_apple_moun(splited_sentence[0]),type(id_apple_moun(splited_sentence[0])))
    #1088 <class 'str'>

    splited_sentence=['been']
    print(id_apple_verbpluspos_vbn_vsimple(splited_sentence[0]),type(id_apple_verbpluspos_vbn_vsimple(splited_sentence[0])))

    splited_sentence = ['continue']
    print(id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[0]),type(id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[0])))

    splited_sentence=['never']
    print(id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[0]),type(id_apple_adverb_word_or_comparative_without_more_or_superlative_without_most(splited_sentence[0])))

    #查看一个单词是否是单性动词的原型
    splited_sentence = ['were']
    print(id_apple_verbpluspos_vori_vsimple(splited_sentence[0]),type(id_apple_verbpluspos_vori_vsimple(splited_sentence[0])))

    #查看一个单词是否是多性动词的原型
    splited_sentence = ['were']
    print(id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[0]),type(id_apple_verbpluspos_double_vori_vcomplex(splited_sentence[0])))

    #查看一个单词是单性动词的原型、三单、现在分词、过去式、过去分词
    splited_sentence = ['be']
    print(id_apple_verbpluspos_vori_vsimple(splited_sentence[0]),id_apple_verbpluspos_vbz_vsimple(splited_sentence[0]),id_apple_verbpluspos_vbg_vsimple(splited_sentence[0]),id_apple_verbpluspos_vbd_vsimple(splited_sentence[0]))