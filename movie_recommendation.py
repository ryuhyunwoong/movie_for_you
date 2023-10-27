import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
import re
from gensim.models import Word2Vec
from konlpy.tag import Okt

def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))
    simScore = sorted(simScore, key = lambda x:x[1], reverse = True)
    simScore = simScore[:11]
    moviIdx = [i[0] for i in simScore]
    recMovieList = df_reviews.iloc[moviIdx, 0]
    return recMovieList

df_reviews = pd.read_csv('./crawling_data2/cleaned_one_review.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

############################## 영화 리뷰 기반 추천##############################
# print(df_reviews.iloc[383, 0])
# cosine_sim = linear_kernel(Tfidf_matrix[383], Tfidf_matrix)
# print(cosine_sim[0])
# print(len(cosine_sim[0]))
# recommendation = getRecommendation(cosine_sim)
# print(recommendation)

# keyword 기반 추천
# embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')
# keyword = '마블'
# try:
#     sim_word = embedding_model.wv.most_similar(keyword, topn = 10)
#     print(sim_word)
#     words = [keyword]
#     for word, _ in sim_word:
#         words.append(word)
#     print(words)
#
#     sentence = []
#     count = 10
#     for word in words:
#         sentence = sentence + [word] * count
#         count -= 1
#     sentence = ' '.join(sentence)
#     print(sentence)
#
#
#     sentence_vec = Tfidf.transform([sentence])
#     cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
#     recommandation = getRecommendation(cosine_sim)
#     print(recommandation)
# except:
#     print('다른 키워드를 이용하세요')

################## 문장 기반 추천 ############################
sentence = '가을의 쓸쓸함을 달래줄 달콤한 사랑 영화'

okt = Okt()
df_stopwords = pd.read_csv('./stopwords.csv')
stopwords = list(df_stopwords['stopword'])

cleaned_sentences = []

word = sentence

word = re.sub('[^가-힣]', ' ', word)
tokened_word = okt.pos(word, stem = True)

df_token = pd.DataFrame(tokened_word, columns = ['word', 'class'])
df_token = df_token[(df_token['class'] == 'Noun') |
                    (df_token['class'] == 'Verb') |
                    (df_token['class'] == 'Adjective')]

words = []
for word in df_token.word:
    if 1 < len(word):
        if word not in stopwords:
            words.append(word)
cleaned_sentence = ' '.join(words)

sentence = cleaned_sentence
print(sentence)

try:
    sentence_vec = Tfidf.transform([sentence])
    cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
    recommandation = getRecommendation(cosine_sim)
    print(recommandation)
except:
    print('다른 키워드를 이용하세요')