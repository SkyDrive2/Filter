import json
from json import load
import re
import copy

# handle activity folder


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# print(bcolors.OKBLUE + "test123" + bcolors.ENDC)


def load_json_folder(folder_road):
    f = open('./' + folder_road + '/projects/index.json', 'r', encoding='utf-8')
    data = json.load(f)
    f.close()
    return data

# compare content with filter


def compare(key_list, content_list):
    value_list = []
    for content in content_list:
        for key in key_list:
            if key in content:
                value_list.append(str(content))

    if len(value_list) == 0:
        return None
    else:
        return list(set(value_list))


def regular_expression(branch_type, content, only_one):
    data = load_json_folder("filter_tool")
    branch = {}
    key_list = data[branch_type].keys()
    # print('\033[95m' + content + '\033[0m')
    # print('\033[93m' + "[OnlyOne]:\t" + str(only_one) + '\033[0m')
    if only_one:
        # print('\033[93m' + "[OnlyOne]"+'\033[0m')
        for output_key in key_list:
            branch[output_key] = None
            for key in data["only_one"][output_key]:
                # print(key, content)
                # input("STOP!!!!")
                findall_list = re.findall(key, content)
                # print("\n" + str(findall_list), end="\n")
                # print("======================")

                if len(findall_list) == 0:
                    findall_list = None
                #     print('\033[96m' + "[KEY]" + key + '\033[0m')
                #     print('\033[91m' + output_key +
                #           " : " + "Not Found" + '\033[0m')
                # else:
                #     print('\033[96m' + "[KEY]" + key + '\033[0m')
                #     print('\033[92m' + output_key + " : " +
                #       str(findall_list) + '\033[0m')
                #     print("========\n")
                # input("Stop\n===========================")
                if branch[output_key] == None:
                    branch[output_key] = findall_list
        return branch
    else:
        # print('\033[93m' + "[Jeneral]"+'\033[0m')
        for output_key in key_list:
            branch[output_key] = None
            for key in data[branch_type][output_key]:
                findall_list = re.findall(key, content)
                if len(findall_list) == 0:
                    findall_list = None
                
                    # print('\033[96m' + "[KEY]" + key + '\033[0m')
                    # print('\033[91m' + output_key +
                    #       " : " + "Not Found" + '\033[0m')
                # else:
                #     print('\033[96m' + "[KEY]" + key + '\033[0m')
                #     print('\033[92m' + output_key + " : " +
                #           str(findall_list) + '\033[0m')
                # print("========\n")
                if branch[output_key] == None:
                    branch[output_key] = findall_list
        return branch


# def build_branch(name , data , content_in_line):
#     branch_dic = {}
#     branch_dic["name"] = name
#     if name != "jeneral" :
#         for line in content_in_line:
#             if not (name in line):
#                 content_in_line.remove(line)
#     branch_dic["apply_start"] = compare(data["apply_start"], content_in_line)
#     branch_dic["apply_end"] = compare(data["apply_end"], content_in_line)
#     branch_dic["apply_fee"] = compare(data["apply_fee"], content_in_line)
#     branch_dic["date_end"] = compare(data["date_end"], content_in_line)
#     branch_dic["date_start"] = compare(data["date_start"], content_in_line)
#     branch_dic["location"] = compare(data["location"], content_in_line)

#     return branch_dic

# all key in output
# 課程網址
# 初賽 複賽 線上賽 線下賽
# 活動訊息

def fil_content(content, dic):
    f = open('./filter_tool/filter_key_words.json', "r", encoding="utf-8")
    data = json.load(f)
    f.close()
    content = content.replace(" ", "")
    content = content.replace("\n", "@")
    dic["content"] = content
    content_in_line = content.split("\n")
    # dic["connection"] = compare(data["connection"], content_in_line)
    # update_sources = compare(data["sources"], content_in_line)
    # if dic["sources"][0] == None :
    #     dic["sources"] = update_sources
    # else :
    #     if update_sources != None:
    #         dic["sources"].append(update_sources)
    # dic["holder"] = compare(data["holder"], content_in_line)
    # dic["image"] = compare(data["image"], content_in_line)
    # dic["object"] = compare(data["object"], content_in_line)
    # dic["subtitle"] = compare(data["subtitle"], content_in_line)
    # dic["tags"] = compare(data["tags"], content_in_line)

    branch_name_list = []
    for branch_name in data["branch_name"]:
        if (branch_name in content):
            branch_name_list.append(branch_name)

    only_one = False
    if len(branch_name_list) == 0:
        branch_name_list.append("jeneral")
    if len(branch_name_list) == 1:
        only_one = True

    # print('\033[92m' + "branch_name_list:\t", branch_name_list, '\033[0m')
    # print(dic["content"])
    for branch_name in branch_name_list:
        dic[branch_name] = regular_expression(
            branch_name, dic["content"], only_one)
        # print(dic[branch_name])
        # input("STOP...")
    # no_jeneral = True
    # for branch_name in data["branch_name"]:
    #     if (branch_name in content):
    #         dic["branch"].append(build_branch(branch_name , data , content_in_line))
    #         no_jeneral = False

    # if no_jeneral :
    #     dic["branch"].append(build_branch("jeneral" , data , content_in_line))

    return

# handle index.json


def fil_obj(obj):
    out_dic = {}
    out_dic["title"] = obj["title"]
    # out_dic["sources"] = [obj["url"]]
    # out_dic["date"] = obj["date"]
    fil_content(obj["content"], out_dic)
    return out_dic


# write output json
with open('./filter_tool/filter_after.json', 'w', encoding='utf-8') as jsonfile:
    load_folder_list = load_json_folder(
        "peaceHighSchool") + load_json_folder("camping") + load_json_folder("developerWeb")
    out_list = []
    for obj in load_folder_list:
        out_list.append(fil_obj(obj))
    # test id
    m = 0
    for all in out_list:
        all["id"] = m
        m = m + 1
        
        # if "jeneral" in all.keys():
        #     if(all["jeneral"]["date_start"] == None):
        #         print(bcolors.OKBLUE + all["content"] + bcolors.ENDC)
        #         print(bcolors.WARNING + "[date_start]" +bcolors.ENDC)
        #         print(bcolors.OKGREEN + str(all["id"]) + bcolors.ENDC)
        #         print(bcolors.BOLD + str(all) + bcolors.ENDC)
        #         print("=================================")
        #         input("Stop\n\n\n")
    # print(all)
    json.dump(out_list, jsonfile, ensure_ascii=False, indent=4)
jsonfile.close()

# update only_one


def update_only_one():
    a = open("./filter_tool/projects/index.json", 'r', encoding='utf-8')
    c = json.load(a)
    a.close()
    k = c.keys()
    # print(type(k))

    only_dic = {}
    # print(c["初賽"].keys())
    # print(k)
    for all in c["初賽"].keys():
        li = []
        for te in k:
            for con in c[te][all]:
                li.append(con)
            # print(c[te][all])
        # print(type(li))
        # sdf = copy.deepcopy(li)
        # print(sdf)
        only_dic[all] = list(set(copy.deepcopy(li)))
        li.clear()
    # print(only_dic)
    out = {}
    for name in k:
        out[name] = c[name]
    out["only_one"] = only_dic
    b = open("./filter_tool/projects/index.json", "w", encoding="utf-8")
    json.dump(out, b, ensure_ascii=False, indent=4)
    b.close()


update_only_one()
# /３、決賽辦理：111年11月12日（星期六）假新北市立清水高中辦理。
# apply_int_site:報名網址 上網登錄報名 處理進soureces
# 照片Image{image_url image_alt}
# branch
# 報名表單
# 命名
