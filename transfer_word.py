def transfer_every_word_in_list_to_lower(splited_sentence:list):
    new_splited_sentence = []
    for i in range(len(splited_sentence)):
        new_splited_sentence.append(splited_sentence[i].lower())
    return new_splited_sentence
