import re
key = ["高中生", "高職生", "所有參賽者皆須持有中華民國國民身份證或本國居留證", "大專院校", "進修部", "碩、博士", "在職專班", "在臺就學之外籍學生", "高中職學生", "高中職生",
       "居住臺、澎、金、馬之中華民國國民", "五專", "高中職學校", "國小", "國中", "國民小學學生", "高中職師生", "中華民國各縣(市)公、私立學校之學生", "公、私立國民小學就讀中之學生"]


def ObjectiveFilter(content):
    objectiveList = []
    for i in key:
        if len(re.findall(i, content)) != 0:
            objectiveList.append(i)
    if len(objectiveList) == 0:
        return None
    else:
        return objectiveList
