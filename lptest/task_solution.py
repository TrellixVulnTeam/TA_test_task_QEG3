import pandas as pd
import pymorphy2
from collections import Counter
import string
import csv
import re

import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel

file_path = "/Users/arslanrashidov/Downloads/covid_tweets.csv.gz"
stop_words_path = "/Users/arslanrashidov/Desktop/Документы/lptest/stopwords-ru.txt"


def main():
    global stop_words
    global words_count
    global data_lemmatized
    data_lemmatized = []
    stop_words = get_stop_words()
    words_count = Counter()

    df = pd.read_csv(file_path, compression="gzip")

    lemmatizeDF(df)
    delete_wordsLess5()
    words_count = words_count.most_common()
    delete_words_count_wordsLess5()
    writeWordsCSV(words_count)

    print(data_lemmatized)
    makingLDA()


def lemmatizeDF(
        df):  # функция, которая выполняет лемматизацию слов корпуса, удаляет стоп-слова, подсчитывает частоту слов
    morph = pymorphy2.MorphAnalyzer()
    tt = str.maketrans(dict.fromkeys(string.punctuation))


    for i in range(len(df["text"])):
        text = df["text"][i]
        words = text.split()
        res = list()

        for word in words:
            if "@" not in word:
                word = deEmojify(word.translate(tt))
                p = morph.parse(word)[0]  # леммат
                if p.normal_form not in stop_words and p.normal_form != '':  # удаляем стоп-слова
                    res.append(p.normal_form)

        data_lemmatized.append(res)

        for word in res:
            words_count[word.strip().lower()] += 1

        print("Completed:" + str(i) + "/" + str(len(df["text"])) + "(1)")


def delete_wordsLess5():  # функция, которая удаляет слова, частота которых <5
    i = 0
    count = 0
    count_words = len(data_lemmatized)
    while i < len(data_lemmatized):
        text = data_lemmatized[i]
        j = 0
        while j < len(text):
            if words_count[text[j]] < 5:
                del (text[j])
            else:
                j += 1

        if len(text) == 0:
            del (data_lemmatized[i])
        else:
            i += 1

        print("Completed:" + str(count) + "/" + str(count_words) + "(2)")
        count += 1


def makingLDA():
    id2word = corpora.Dictionary(data_lemmatized)
    texts = data_lemmatized
    corpus = [id2word.doc2bow(text) for text in texts]
    print("lda20 started")
    lda_model20 = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                  id2word=id2word,
                                                  num_topics=20,
                                                  random_state=100,
                                                  update_every=1,
                                                  chunksize=80,
                                                  passes=10,
                                                  alpha='auto',
                                                  per_word_topics=True)
    print("lda20 completed")
    topics20 = lda_model20.print_topics(num_topics=20, num_words=20)
    writeWordsTXT(topics20, "lda20.txt")
    print("lda30 started")
    lda_model30 = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                  id2word=id2word,
                                                  num_topics=30,
                                                  random_state=200,
                                                  update_every=1,
                                                  chunksize=80,
                                                  passes=10,
                                                  alpha='auto',
                                                  per_word_topics=True)
    print("lda30 completed")
    topics30 = lda_model30.print_topics(num_topics=30, num_words=20)
    writeWordsTXT(topics30, "lda30.txt")
    print("lda50 started")
    lda_model50 = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                  id2word=id2word,
                                                  num_topics=50,
                                                  random_state=300,
                                                  update_every=1,
                                                  chunksize=80,
                                                  passes=10,
                                                  alpha='auto',
                                                  per_word_topics=True)
    print("lda50 completed")
    topics50 = lda_model50.print_topics(num_topics=50, num_words=20)
    writeWordsTXT(topics50, "lda50.txt")

def delete_words_count_wordsLess5():
    print(words_count)
    i = 0
    while i < len(words_count):
        print(words_count[i])
        print(words_count[i][1])
        if words_count[i][1] < 5:
            del(words_count[i])
        else:
            i+=1



def get_wordsInTopics(topics):
    all_words_in_topics = []

    for i in range(len(topics)):
        words_in_topic = []
        words = topics[i][1].split('"')
        for j in range(1, len(words), 2):
            words_in_topic.append(words[j])
        all_words_in_topics.append(words_in_topic)

    return all_words_in_topics


def get_stop_words():  # функция, которая получает стоп-слова
    massive_of_words = []
    file1 = open(stop_words_path, "r")
    while True:
        line = file1.readline().rstrip('\n')
        if not line:
            break

        massive_of_words.append(line)
    file1.close
    return massive_of_words


def deEmojify(text):  # функция, которая возвращает строку без смайликов
    regrex_pattern = re.compile(pattern="["
                                        u"\U0001F600-\U0001F64F"
                                        u"\U0001F300-\U0001F5FF"
                                        u"\U0001F680-\U0001F6FF"
                                        u"\U0001F1E0-\U0001F1FF"
                                        "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)


def writeWordsCSV(cnt):  # функция, которая записывает слова в csv-файл
    with open("wordsCount.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(cnt)


def writeWordsTXT(topics, file_path):  # функция, которая записывает слова в txt-файл
    topics = get_wordsInTopics(topics)
    with open(file_path, "w") as file:
        for topic in topics:
            file.write(' '.join(topic) + '\n')


main()
