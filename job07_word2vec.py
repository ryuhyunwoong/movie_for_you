import pandas as pd
from gensim.models import Word2Vec

df_review = pd.read_csv('./crawling_data2/cleaned_one_review.csv')
df_review.info()

reviews = list(df_review['reviews'])
print(reviews[0])

tokens = []
for sentence in reviews:
    token = sentence.split()
    tokens.append(token)
print(tokens[0])

embedding_model = Word2Vec(tokens, vector_size = 100, window = 4, # 커널 사이즈
                           min_count = 20,  # 20번 이상 나오는 단어만 학습
                           workers = 16, # 사용할 cpu 프로세서 갯수 설정
                           epochs=100, sg = 1) # skip gram
embedding_model.save('./models/word2vec_movie_review.model')
print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))