import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
##TF-IDF는 특정 단어가 문서 내에서 얼마나 중요한지를 계산하는 데 사용되는 통계적 측정 방법입니다.
##이 방법은 자연어 처리 분야에서 널리 사용되며, 특히 문서의 핵심 단어 추출, 검색 엔진, 문서 분류 및 군집화 등과 같은 다양한 텍스트 마이닝 작업에 활용됩니다.
from scipy.io import mmwrite, mmread
import pickle

df_reviews = pd.read_csv('./crawling_data/cleaned_one_review.csv')
df_reviews.info()

Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews['reviews'])
print(Tfidf_matrix.shape)

with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)

mmwrite('./models/Tfidf_movie_review.mtx', Tfidf_matrix)