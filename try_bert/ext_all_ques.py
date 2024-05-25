from docx import Document
import os

def get_ques_list(folder):
    os.chdir(folder)
    list_of_files = os.listdir()
    all_ques = {}
    for filename in list_of_files:
        if(filename[len(filename)-5:] == '.docx'):
            doc = Document(filename)
            # print(filename)
            # print(doc)

            fullText = []
            for para in doc.paragraphs:
                # print(para.text)
                fullText.append(para.text)
            # doctxt =  '\n'.join(fullText)
            doctxt = fullText
            fullText = []
            for eachl in doctxt:
                # print(eachl)
                if len(eachl) == 0:
                    continue
                elif eachl[0] == 'Q':
                    fullText.append(eachl.split(" ", 1)[1])   # for networking "." -> " "
                else:
                    fullText[len(fullText)-1] = fullText[len(fullText)-1] + ' ' + eachl

            all_ques[filename[:len(filename)-5]] = fullText
            # all_ques = all_ques + fullText
            # print(doctxt)
            # print(fullText)
    os.chdir("..")
    return all_ques



if __name__ == "__main__":
    os.chdir("../theory")
    print(os.getcwd())
    print(get_ques_list("DBMS"))
    for key, value in get_ques_list("DBMS").items():
        print(key)
        for val in value:
            print(val)
        print()

    # os.chdir("./networking")
    # list_of_files = os.listdir()
    # file = "Amazon.docx"
    # for file in list_of_files:
    #     ques = get_ques_list(file)
    #     print(file)
    #     print(ques)
    #     print()
