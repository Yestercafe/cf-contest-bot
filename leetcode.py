import requests
import json

class LCProblem:
    def __init__(self, no: str, slug: str, level: str, title: str, url: str):
        self.no = no
        self.slug = slug
        self.level = level
        self.title = title
        self.url = url

def get_daily_url() -> LCProblem:
    base_url = 'https://leetcode.cn'
    response = requests.post(base_url + "/graphql", json={
        "operationName": "questionOfToday",
        "variables": {},
        "query": "query questionOfToday { todayRecord {   question {     questionFrontendId     questionTitleSlug     __typename   }   lastSubmission {     id     __typename   }   date   userStatus   __typename }}"
    })
    slug = json.loads(response.text).get('data').get('todayRecord')[0].get("question").get('questionTitleSlug')

    url = base_url + "/problems/" + slug
    response = requests.post(base_url + "/graphql",
                            json={"operationName": "questionData", "variables": {"titleSlug": slug},
                                "query": "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    questionFrontendId    boundTopicId    title    titleSlug    content    translatedTitle    translatedContent    isPaidOnly    difficulty    likes    dislikes    isLiked    similarQuestions    contributors {      username      profileUrl      avatarUrl      __typename    }    langToValidPlayground    topicTags {      name      slug      translatedName      __typename    }    companyTagStats    codeSnippets {      lang      langSlug      code      __typename    }    stats    hints    solution {      id      canSeeDetail      __typename    }    status    sampleTestCase    metaData    judgerAvailable    judgeType    mysqlSchemas    enableRunCode    envInfo    book {      id      bookName      pressName      source      shortDescription      fullDescription      bookImgUrl      pressImgUrl      productUrl      __typename    }    isSubscribed    isDailyQuestion    dailyRecordStatus    editorType    ugcQuestionId    style    __typename  }}"})
    jsonText = json.loads(response.text).get('data').get("question")
    no = jsonText.get('questionFrontendId')
    title = jsonText.get('translatedTitle')
    level = jsonText.get('difficulty')
    return LCProblem(no=no, slug=slug, level=level, title=title, url=url)
