from try_scrape import ques
from pandas import DataFrame
import csv
import os

def saveques(filename):
    problem_statement = []
    titleslug = []
    title = []
    single_tag = []
    multi_tags = []
    num_occur = []
    with open(filename, "r") as file_obj:
        heading = next(file_obj)
        dataa = csv.reader(file_obj)
        # print(heading)
        for data in dataa:
            data[0] = data[0].split("problems/")[1]
            data[0] = data[0][:len(data[0]) - 1]
            try:
                tt, qs, tags = ques(data[0])
                qs = ' '.join(qs.split('\n'))
                problem_statement.append(qs)
                titleslug.append(data[0])
                title.append(tt)
                single_tag.append(tags[0])
                multi_tags.append(', '.join(tags))
                num_occur.append(data[2])

                print(data[0])
                print(tt)
                print(qs)
                print(multi_tags)
                print(problem_statement)
                print()
            except:
                pass

    dict = {'problem_statement': problem_statement, 'titleslug': titleslug, 'title': title, 'tags': single_tag, 'num_occur': num_occur}
    dict_multi = {'problem_statement': problem_statement, 'titleslug': titleslug, 'title': title, 'tags': multi_tags, 'num_occur': num_occur}
    df = DataFrame(dict)
    df.to_csv('with_ques/'+filename, index=False)
    df = DataFrame(dict_multi)
    df.to_csv('with_multi_tags/'+filename, index=False)


if __name__ == "__main__":
    os.chdir("coding")
    files = os.listdir()
    print(files)
    for file in files:
        if(file[len(file)-4:] == '.csv'):
            saveques(file)