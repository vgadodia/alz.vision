from similarity import text_similarity

def similarity_score(sentence1, sentence2):
    percentage = text_similarity.token_set_ratio(sentence1, sentence2)
    percentage = float(percentage)/100
    return percentage

sent1 = "THIS IS A REDESCRIPTION OF THE PARTY"
sent2 = "THIS IS A DESCRIPTION"

# print(similarity_score(sent1, sent2))