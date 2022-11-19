import json
import re
import copy
import datetime
# load folder which is under projects


def load_json_folder(folder_road):
    f = open(folder_road, 'r', encoding='utf-8')
    data = json.load(f)
    f.close()
    return data


def update_only_one():
    a = open("./re_filter_tool/projects/branch_key.json", 'r', encoding='utf-8')
    c = json.load(a)
    a.close()
    k = c.keys()
    only_dic = {}
    for all in c["初賽"].keys():
        li = []
        for te in k:
            if te != "OnlyOne":
                for con in c[te][all]:
                    li.append(con)
        only_dic[all] = list(set(copy.deepcopy(li)))
        li.clear()
    out = {}
    for name in k:
        out[name] = c[name]
    out["OnlyOne"] = only_dic
    b = open("./re_filter_tool/projects/branch_key.json", "w", encoding="utf-8")
    json.dump(out, b, ensure_ascii=False, indent=4)
    b.close()


def ex_branch_regular_expression(name, content):

    return


def compare(key_list, content_list, type):
    value_list = []
    for content in content_list:
        for key in key_list:
            if key in content:
                value_list.append(str(key))
    if len(value_list) == 0:
        return None
    else:
        return list(set(value_list))


def tags_filter(content):
    data = load_json_folder('./re_filter_tool/projects/tags_key.json')
    tags_type_list = ["Area", "Location", "Other"]
    tag_list = []
    tag_id = 0
    for type in tags_type_list:
        for tag in data[type]:
            if tag in content:
                tag_dic = {}
                tag_dic["Type"] = type
                tag_dic["TagId"] = tag_id
                # tag_id += 1
                tag_dic["Text"] = tag
                tag_dic["TagCount"] = 0
                tag_list.append(dict(tag_dic))
                tag_dic.clear()
    if len(tag_list) == 0:
        return None
    else:
        return tag_list


def to_date_type(name, list):
    output_list = []
    if list == None:
        return list
    for line in list:
        if (name == "ApplyStart") | (name == "DateStart"):
            if "即日" in line:
                output_list.append("自即日起")
            else:

                split_list = re.split("[^0-9]", line)
                remove_split_list = [i for i in split_list if i != ""]

                if len(remove_split_list) == 3:
                    if int(remove_split_list[0]) < 1911:
                        remove_split_list[0] = str(
                            int(remove_split_list[0])+1911)

                    date = str(datetime.date(int(remove_split_list[0]), int(
                        remove_split_list[1]), int(remove_split_list[2])))
                    output_list.append(date)
                elif len(remove_split_list) == 2:
                    if remove_split_list[1] == 124:
                        output_list.append(line)
                        return output_list
                    remove_split_list.insert(0, "1999")
                    print(remove_split_list)
                    print("============")
                    date = str(datetime.date(int(remove_split_list[0]), int(
                        remove_split_list[1]), int(remove_split_list[2])))
                    output_list.append(date)
                else:
                    output_list.append(line)
        elif (name == "ApplyEnd") | (name == "DateEnd"):
            return list
    return output_list


def regular_expression(branch_name, content, only_one):
    data = load_json_folder('./re_filter_tool/projects/branch_key.json')
    branch = {}
    to_datetype_name = ["DateStart", "DateEnd", "ApplyStart", "ApplyEnd"]
    key_list = data[branch_name].keys()
    branch["BranchName"] = branch_name
    if only_one:
        branch_name = "OnlyOne"
    for output_key in key_list:
        branch[output_key] = None
        for key in data[branch_name][output_key]:
            findall_list = re.findall(key, content)
            # print(findall_list)
            if len(findall_list) == 0:
                findall_list = None
            if branch[output_key] == None:
                branch[output_key] = findall_list
            elif findall_list != None:
                for compare_twice in findall_list:
                    if not (compare_twice in branch[output_key]):
                        branch[output_key].append(compare_twice)
        # if output_key in to_datetype_name:
        #     branch[output_key] = to_date_type(output_key,branch[output_key])
    return branch

def fil_branch(content):
    content.replace("\n", "%")
    branch_name_data = ["初賽", "複賽", "決賽", "線上賽", "線下賽"]
    branch_name_list = []
    for branch_name in branch_name_data:
        if (branch_name in content):
            branch_name_list.append(branch_name)

    only_one = False
    if len(branch_name_list) == 0:
        branch_name_list.append("Jeneral")
    if len(branch_name_list) == 1:
        only_one = True

    branch_dic = {}
    for branch_name in branch_name_list:
        branch_dic["Branches"] = regular_expression(
            branch_name, content, only_one)
    return branch_dic


def fil_ex_branch(content, ori_sources):
    data = load_json_folder('./re_filter_tool/projects/ex_branch_key.json')
    ex_branch_dic = {}
    content = "%"+ content.replace("\n","%↑%") +"%"
    content_list = content.split("↑")
    ex_branch_name_data = ["Connection", "Holder","Location","Objective","Sources","Subtitle"]
    for key in ex_branch_name_data:
        ex_branch_dic[key] = []
        for value in data[key]:
            for content_in_line in content_list:
                findall_list = re.findall(value,content_in_line)
                if len(findall_list)!= 0:
                    ex_branch_dic[key].extend(findall_list)
        if len(ex_branch_dic[key]) == 0:
            ex_branch_dic[key] = None
    if ex_branch_dic["Sources"] != None:
        ex_branch_dic["Sources"] = ex_branch_dic["Sources"] + ori_sources
    else:
        ex_branch_dic["Sources"] = ori_sources
    if len(ex_branch_dic["Sources"]) == 0:
        ex_branch_dic["Sources"] = None
    return ex_branch_dic
    


def obj_filter(obj_dic):
    output_dic = {}
    output_dic["Title"] = obj_dic["title"]
    tem_sources = []
    url_list = [obj_dic["url"]]
    source_url_list = [obj_dic["source_url"]]
    if (url_list[0] != None) and (source_url_list[0] != None):
        tem_sources = url_list + source_url_list
        
    elif (url_list[0] == None) and (obj_dic["source_url"] == None):
        tem_sources = []
    else:
        if obj_dic["url"] != None:
            tem_sources = url_list
        else: 
            tem_sources = source_url_list
    output_dic["Content"] = obj_dic["content"].replace(" ", "")
    if "imag" in obj_dic.keys():
        output_dic["Image"] = obj_dic["image"]
    # output_dic["Date"] = obj_dic["date"]
    output_dic.update(fil_ex_branch(output_dic["Content"],tem_sources))
    output_dic.update(fil_branch(output_dic["Content"]))
    return output_dic


# write output json
with open('./re_filter_tool/filter_after.json', 'w', encoding='utf-8') as jsonfile:
    folder_list = ["peaceHighSchool", "camping", "developerWeb"]
    load_folder_list = []
    for folder_name in folder_list:
        folder_name = './' + folder_name + '/projects/index.json'
        load_folder_list += load_json_folder(folder_name)

    output_list = []
    ActivityId = 0
    for each_obj in load_folder_list:
        output_list.append(obj_filter(each_obj))
        output_list[ActivityId]["ActivityId"] = 0
        ActivityId += 1

    json.dump(output_list, jsonfile, ensure_ascii=False, indent=4)
jsonfile.close()

update_only_one()


# filter date from original floder["date"]


# filter "Tags" in except_branch_dic
