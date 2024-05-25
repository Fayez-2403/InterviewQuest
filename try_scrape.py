import requests
from bs4 import BeautifulSoup as bs


def ques(titleslug):
    data = {"operationName": "questionData", "variables": {"titleSlug": titleslug},
            "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    "
                     "questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n   "
                     " translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    "
                     "dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      "
                     "profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags "
                     "{\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n "
                     "   codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n "
                     "   hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n   "
                     " sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    "
                     "enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}

    r = requests.post('https://leetcode.com/graphql', json=data).json()
    # print(r)
    soupq = bs(r['data']['question']['content'], 'lxml')
    soupt = r['data']['question']['topicTags']
    tags = []
    for it in soupt:
        tags.append(it["name"])
    # print(soupt)
    title = r['data']['question']['title']
    question = soupq.get_text()
    question = question.split("\nExample")[0]
    return title, question, tags


if __name__ == "__main__":
    title, ques, tags = ques("lru-cache")
    print(title)
    print(ques)
    print(tags)
