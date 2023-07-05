import mydb
import split_sentence_to_list
import predicate
import judegclause

if __name__ == '__main__':
   splited_sentence = split_sentence_to_list.split_sentence_to_list("Therefore, this cannot be the responsibility of parents alone.")
   print(predicate.check_priority_one_one(splited_sentence))