from try_scrape import ques
from pandas import read_csv
import os

os.chdir("coding")

links = read_csv("Amazon.csv")
links = links["problem_link"].tolist()
for i in range(len(links)):
    links[i] = links[i].split("problems/")[1]
    links[i] = links[i][:len(links[i])-1]
    print(links[i])
    title, question, tags = ques(links[i])
    print(title)
    print(question)
    print(tags)
    print()

# print(links)



