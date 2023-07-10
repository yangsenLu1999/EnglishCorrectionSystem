import  split_sentence_to_list
import split_structure
if __name__ == '__main__':
    sentence = "Under certain cultures, children"
    splited_sentence = split_sentence_to_list.splited_sentence(sentence)
    print(splited_sentence)
    # for i in range(len(new_splited_sentence) - 1, -1, -1):
    #     if ',' in new_splited_sentence[i]:
    #         print(f"列表中最右边包含逗号的元素的索引为 {i}")
    #         right_comma_index = i
    #         print(right_comma_index)
    #         break
    #     else:
    #         print("列表中没有包含逗号的元素")
    # print(splited_sentence)
    # Subject_Dict=split_structure.traverse_the_list_to_get_the_first_subject_structure(splited_sentence)
    # print(Subject_Dict)
    # print(Subject_Dict['subject'])
