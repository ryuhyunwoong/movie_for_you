import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/merge_reviews_professor.csv')
df.info()

okt = Okt()

## stopwords파일로 불용어 리스트 생성
df_stopwords = pd.read_csv('./stopwords.csv')
stopwords = list(df_stopwords['stopword'])

## 텍스트 전처리
count = 0
cleaned_sentences = []

## review열 반복하여 불용어 제외한 단어 추출하여 cleaned_sentences리스트에 추가
for review in df.review:
    count += 1
    if count % 100 == 0:
        print('.', end='')
    if count % 1000 == 0:
        print()
    if count % 10000 == 0:
        print(count / 10000, end='')
    review = re.sub('[^가-힣]', ' ', review)
    tokened_review = okt.pos(review, stem=True)

    df_token = pd.DataFrame(tokened_review, columns=['word', 'class'])
    df_token = df_token[(df_token['class']=='Noun') |
                        (df_token['class']=='Verb') |
                        (df_token['class']=='Adjective')]
    words = []
    for word in df_token.word:
        if 1 < len(word):
            if word not in stopwords:
                words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)


df['cleaned_sentences'] = cleaned_sentences
df = df[['title', 'cleaned_sentences']]
print(df.head(10))
df.info()

df.to_csv('./crawling_data/cleaned_review.csv', index=False)