##[0, 0] 관상 --> 리뷰비슷한 영화 찾아보기!! / 2-번줄과 2-번줄 인덱스값을 영화 번호로 바꾸면 됨

import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
import re
from gensim.models import Word2Vec

def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))
    simScore = sorted(simScore, key=lambda  x:x[1], reverse=True)
    simScore = simScore[:11]
    moviIdx = [i[0] for i in simScore]
    recMovieList = df_reviews.iloc[moviIdx, 0]
    return recMovieList

df_reviews = pd.read_csv('./crawling_data/cleaned_one_review.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)
## 영화 리뷰기반 추천 (인덱스값에 영화 번호 입력시) ##
# print(df_reviews.iloc[1095, 0])
#
# cosine_sim = linear_kernel(Tfidf_matrix[1095], Tfidf_matrix)
# print(cosine_sim[0])
# print(len(cosine_sim[0]))
# recommendation = getRecommendation(cosine_sim)
# print(recommendation)

## keyword기반 추천(단어) ##
# embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')
# keyword = '주식'
# sim_word = embedding_model.wv.most_similar(keyword, topn=10)
# print(sim_word)
# words = [keyword]
# for word, _ in sim_word:
#     words.append(word)
# print(words)
#
# sentence = []
# count = 10
# for word in words:
#     sentence = sentence + [word] * count
#     count -= 1
# sentence = ' '.join(sentence)
# print(sentence)
# sentence_vec = Tfidf.transform([sentence])
# cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
# recommendation = getRecommendation(cosine_sim)
# print(recommendation)


## 문장기반으로 추천 해주기 ##
okt = Okt()

sentence = '겨울에 잘 어울리는 영화'
sentence = re.sub('[^가-힣]',' ',sentence)
tokened_sentence = okt.pos(sentence, stem=True)

df_token = pd.DataFrame(tokened_sentence, columns = ['word','class'])
df_token = df_token[(df_token['class']=='Noun') |
                    (df_token['class']=='Verb') |
                    (df_token['class']=='Adjective')]

df_stopwords = pd.read_csv('stopwords.csv')
stopwords = list(df_stopwords['stopword'])

keywords = []
for word in df_token.word:
    if len(word) > 1 and word not in stopwords:
        keywords.append(word)

embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')

sim_words = []
for keyword in keywords:
    try:
        sim_word = embedding_model.wv.most_similar(keyword, topn=10)
        for word, _ in sim_word:
            sim_words.append(word)
    except:
        continue
print(sim_words)
sentence = ' '.join(sim_words)
print(sentence)
sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation)










