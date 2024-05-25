import csv
import os
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import re
# nltk.download('stopwords')
# nltk.download('omw-1.4')
# nltk.download('wordnet')
# wn = nltk.WordNetLemmatizer()

def cleanHtml(sentence):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', str(sentence))
    return cleantext


def cleanPunc(sentence): #function to clean the word of any punctuation or special characters
    cleaned = re.sub(r'[?|!|\'|"|#]',r'',sentence)
    cleaned = re.sub(r'[.|,|)|(|\|/]',r' ',cleaned)
    cleaned = cleaned.strip()
    cleaned = cleaned.replace("\n"," ")
    return cleaned


def keepAlpha(sentence):
    alpha_sent = ""
    for word in sentence.split():
        alpha_word = re.sub('[^a-z A-Z]+', ' ', word)
        alpha_sent += alpha_word
        alpha_sent += " "
    alpha_sent = alpha_sent.strip()
    return alpha_sent

stop_words = set(stopwords.words('english'))
stop_words.update(['zero','one','two','three','four','five','six','seven','eight','nine','ten','may','also','across','among','beside','however','yet','within'])
re_stop_words = re.compile(r"\b(" + "|".join(stop_words) + ")\\W", re.I)
def removeStopWords(sentence):
    global re_stop_words
    return re_stop_words.sub(" ", sentence)

stemmer = SnowballStemmer("english")
def stemming(sentence):
    stemSentence = ""
    for word in sentence.split():
        stem = stemmer.stem(word)
        stemSentence += stem
        stemSentence += " "
    stemSentence = stemSentence.strip()
    return stemSentence

def get_ques(filename):
    df = pd.read_csv(filename)
    print(df)
    df['problem_statement'] = df['problem_statement'].str.lower()
    df['problem_statement'] = df['problem_statement'].apply(cleanHtml)
    df['problem_statement'] = df['problem_statement'].apply(cleanPunc)
    df['problem_statement'] = df['problem_statement'].apply(keepAlpha)
    df['problem_statement'] = df['problem_statement'].apply(removeStopWords)
    df['problem_statement'] = df['problem_statement'].apply(stemming)
    # df['problem_statement'] = df['problem_statement'].apply(lambda x: ' '.join([wn.lemmatize(w) for w in gensim.utils.simple_preprocess(x) if w not in gensim.parsing.preprocessing.STOPWORDS and len(w) > 2]))
    return df['problem_statement']     # .tolist()

if __name__ == "__main__":
    os.chdir("../coding")
    os.chdir("./with_ques")
    # print(get_ques("Amazon.csv"))
    for ques in get_ques("Amazon.csv"):
        print(ques)
 


