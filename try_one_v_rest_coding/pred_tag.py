import csv
import os
import joblib
import pickle
from ext_ques_csv import get_ques
import pandas
import torch
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.feature_selection import SelectKBest, mutual_info_classif

# from sklearn.feature_extraction.text import TfidfVectorizer
# vectorizer = TfidfVectorizer(strip_accents='unicode', analyzer='word', ngram_range=(1,3), norm='l2')

def pred(filename):
    ques_list = get_ques(filename)
    # ques_list = ['given string binary example lkadnf sdfjsn rgrth hgvgvh gvhgv hgvghv hbghvghv jghvjvg gvhgv jbhbvhjj jgjyg yftc ftyyt dfrdrtd', '4tguy3gy 3ugy3tg 3rg3gf3']
    cur_folder = os.getcwd().split('\\').pop()
    # os.chdir('..')

    vectorizer = ''
    with open('../code_vector.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    model = torch.load('../model_final.pt')

    # os.chdir(cur_folder)

    # for each_ques in ques_list:
    #     list_for_vector = []
    #     list_for_vector.append(each_ques)
    #     test = vectorizer.transform([each_ques])
    #
    #     print("Question : ", each_ques)
    #     for category, mdl in model.items():
    #         print(test)
    #         prediction = mdl.predict(test)
    #         print(category)
    #         if prediction[0] == 1:
    #             print(category, end=', ')
    #     print()

    # print(type(ques_list))
    # vectorizer.fit(ques_list)
    test = vectorizer.transform(ques_list)


    test_sparse = pd.SparseDataFrame(test, default_fill_value=0)

    # Convert the sparse dataframe to a sparse matrix
    test_sparse_matrix = csr_matrix(test_sparse.to_coo())

    # Select the top 100 features based on mutual information
    selector = SelectKBest(mutual_info_classif, k=229)
    X_test_selected = selector.fit_transform(test_sparse_matrix, y=[0] * test_sparse_matrix.shape[0])

    for category, mdl in model.items():
        prediction = mdl.predict(X_test_selected)
        print(prediction)
 

if __name__ == "__main__":
    os.chdir("../coding/with_ques")
    pred("Amazon.csv")
