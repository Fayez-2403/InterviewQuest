import csv
import pandas
import pandas as pd

f = open("DBMS n.txt", encoding="utf8")
para = f.read()
#  print(para)
para = para.split("\\n")
# print(para)

df = pd.DataFrame(data=para, columns=["review"])

df.to_csv("DBMS_unfilter.csv", index=False)
