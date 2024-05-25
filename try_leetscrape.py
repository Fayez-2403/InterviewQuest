from leetscrape.GetQuestionsList import GetQuestionsList
from leetscrape.GetQuestionInfo import GetQuestionInfo
from leetscrape.utils import combine_list_and_info, get_all_questions_body

ls = GetQuestionsList()
print(ls)
ls.scrape()
print(ls)
ls.to_csv("data.csv")
