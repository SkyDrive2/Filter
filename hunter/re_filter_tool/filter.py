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
                tag_dic["Id"] = tag_id
                # tag_id += 1
                tag_dic["Text"] = tag
                tag_dic["TagCount"] = 0
                tag_list.append(dict(tag_dic))
                tag_dic.clear()
    if len(tag_list) == 0:
        return None
    else:
        return tag_list


def del_open_character(findall_list):
    tem = ""
    lineopen = ["一", "二", "三", "四", "五", "六", "七", "八", "九",
                "十", "壹", "貳", "參", "肆", "伍", "陸", "柒", "捌", "玖", "拾"]
    if findall_list[0][0] == "(" and findall_list[0][1] in lineopen and findall_list[0][2] == ")":
        for i in range(3, len(findall_list[0])):
            tem += findall_list[0][i]
        findall_list[0] = tem
    elif findall_list[0][0] in lineopen and findall_list[0][1] == "、":
        for i in range(2, len(findall_list[0])):
            tem += findall_list[0][i]
        findall_list[0] = tem
    elif findall_list[0][1] in lineopen and findall_list[0][2] == "、":
        for i in range(3, len(findall_list[0])):
            tem += findall_list[0][i]
        findall_list[0] = tem


def to_date_type(name, li, content):
    if li == None:
        return li
    list2 = []
    check = True
    for i in range(0,len(li)):
        for j in range(0,len(li)):
            if i != j :
                if (li[i] in li[j]):
                    check = False
        if check:
            list2.append(li[i])
        check = True   
    li = list2
    if name == "DateStart":
        datestart_dic = {}
        space = ""
        GeneralDateStart = "GeneralDateStart"
        for line in li:
            find_key_name = re.findall(
                "[\u4E00-\u9FFF^報][\u4E00-\u9FFF^名]日期", line)
            split_list = re.split("[^0-9]", line)
            remove_split_list = [i for i in split_list if i != ""]
            date = ""
            try:
                if "即日" in line:
                    datestart_dic[GeneralDateStart] = "自即日起"
                    GeneralDateStart += "."
                    continue
                elif len(remove_split_list) == 2:
                    year4 = re.findall(
                        "[^0-9]{0,1}[0-9]{4}年", content)
                    year3 = re.findall(
                        "[^0-9]{0,1}[0-9]{3}年", content)
                    if len(year4) != 0:
                        year = re.findall("[0-9]{4}", year4[0])
                        date = str(datetime.date(int(year[0]), int(remove_split_list[0]), int(
                            remove_split_list[1])))
                    elif len(year3) != 0:
                        year = re.findall("[0-9]{3}", year3[0])
                        date = str(datetime.date(int(year[0])+1911, int(remove_split_list[0]), int(
                            remove_split_list[1])))
                elif len(remove_split_list) == 3:
                    if int(remove_split_list[0]) < 1911:
                        remove_split_list[0] = str(
                            int(remove_split_list[0])+1911)
                    date = str(datetime.date(int(remove_split_list[0]), int(
                        remove_split_list[1]), int(remove_split_list[2])))
                else:
                    date = line

            except ValueError:
                date = line
            findkey = ["決賽", "初賽", "線上賽", "線下賽"]
            if len(find_key_name) == 0:
                for name in findkey:
                    if name in line:
                        find_key_name = [name]
            if len(find_key_name) != 0:
                datestart_dic[space + find_key_name[0]] = date
                space += "G"
            else:
                datestart_dic[GeneralDateStart] = date
                GeneralDateStart += "."

        # if len(datestart_dic["GeneralDateStart"]) == 0:
        #     del datestart_dic["GeneralDateStart"]
        return datestart_dic

    if name == "ApplyStart":
        date = ""
        returnlist = []
        for line in li:
            split_list = re.split("[^0-9]", line)
            remove_split_list = [i for i in split_list if i != ""]
            try:
                if "即日" in line:
                    returnlist.append("自即日起")
                    continue
                elif len(remove_split_list) == 2:
                    year4 = re.findall(
                        "[^0-9]{0,1}[0-9]{4}[年]", content)
                    year3 = re.findall(
                        "[^0-9]{0,1}[0-9]{3}[年]", content)
                    if len(year4) != 0:
                        year = re.findall("[0-9]{4}", year4[0])
                        date = str(datetime.date(int(year), int(remove_split_list[0]), int(
                            remove_split_list[1])))
                    elif len(year3 != 0):
                        year = re.findall("[0-9]{3}", year3[0])
                        date = str(datetime.date(int(year)+1911, int(remove_split_list[0]), int(
                            remove_split_list[1])))

                elif len(remove_split_list) == 3:
                    if int(remove_split_list[0]) < 1911:
                        remove_split_list[0] = str(
                            int(remove_split_list[0])+1911)

                    date = str(datetime.date(int(remove_split_list[0]), int(
                        remove_split_list[1]), int(remove_split_list[2])))
                else:
                    date = line

            except:
                date = line
            returnlist.append(date)
            # returnlist.clear()
        # list(dict.fromkeys(returnlist))
        return returnlist
    if name == "DateEnd" or name == "ApplyEnd":
        date = ""
        returnlist = []
        to_key = ["到.{0,20}", "至.{0,20}", "-.{0,20}", "~.{0,20}", "test"]
        for line in li:
            afterline = []
            for keys in to_key:
                if len(afterline) == 0:
                    afterline = re.findall(keys, line)

                else:
                    split_list = re.split("[^0-9]", afterline[0])
                    remove_split_list = [i for i in split_list if i != ""]
                    try:
                        if len(remove_split_list) == 1:
                            test1 = re.findall("[0-9]{4}年[0-9]{1,2}月", line)
                            test2 = re.findall("[0-9]{4}/[0-9]{1,2}", line)
                            test3 = re.findall("[0-9]{3}年[0-9]{1,2}月", content)
                            test4 = re.findall("[0-9]{3}/[0-9]{1,2}", content)
                            if len(test1) != 0:
                                split_list = re.split(
                                    "[^0-9]", test1[0] + afterline[0])
                                remove_split_list = [
                                    i for i in split_list if i != ""]
                                date = str(datetime.date(int(remove_split_list[0]), int(
                                    remove_split_list[1]), int(remove_split_list[2])))
                            elif len(test2) != 0:
                                split_list = re.split(
                                    "[^0-9]", test2[0] + afterline[0])
                                remove_split_list = [
                                    i for i in split_list if i != ""]
                                date = str(datetime.date(int(remove_split_list[0]), int(
                                    remove_split_list[1]), int(remove_split_list[2])))

                            elif len(test3) != 0:
                                split_list = re.split(
                                    "[^0-9]", test3[0] + afterline[0])
                                remove_split_list = [
                                    i for i in split_list if i != ""]
                                date = str(datetime.date(int(
                                    remove_split_list[0])+1911, int(remove_split_list[1]), int(remove_split_list[2])))

                            elif len(test4) != 0:
                                split_list = re.split(
                                    "[^0-9]", test4[0] + afterline[0])
                                remove_split_list = [
                                    i for i in split_list if i != ""]
                                date = str(datetime.date(int(
                                    remove_split_list[0])+1911, int(remove_split_list[1]), int(remove_split_list[2])))
                            returnlist.append(date)
                            break
                        elif len(remove_split_list) == 2:
                            year4 = re.findall(
                                "[^0-9]{0,1}[0-9]{4}[年]", line)
                            year3 = re.findall(
                                "[^0-9]{0,1}[0-9]{3}[年]", line)
                            allyear4 = re.findall(
                                "[^0-9]{0,1}[0-9]{4}[年]", content)
                            allyear3 = re.findall(
                                "[^0-9]{0,1}[0-9]{3}[年]", content)
                            if len(year4) != 0:
                                year = re.findall("[0-9]{4}", year4[0])
                                date = str(datetime.date(int(year[0]), int(remove_split_list[0]), int(
                                    remove_split_list[1])))
                            elif len(year3) != 0:

                                year = re.findall("[0-9]{3}", year3[0])
                                date = str(datetime.date(int(year[0])+1911, int(remove_split_list[0]), int(
                                    remove_split_list[1])))
                            elif len(allyear4) != 0:
                                year = re.findall("[0-9]{4}", allyear4[0])
                                date = str(datetime.date(int(year[0]), int(remove_split_list[0]), int(
                                    remove_split_list[1])))
                            elif len(allyear3) != 0:
                                year = re.findall("[0-9]{3}", allyear3[0])
                                date = str(datetime.date(int(year[0])+1911, int(remove_split_list[0]), int(
                                    remove_split_list[1])))

                        elif len(remove_split_list) == 3:
                            if int(remove_split_list[0]) < 1911:
                                remove_split_list[0] = str(
                                    int(remove_split_list[0])+1911)
                            # print("\033[91m" + remove_split_list[2] + "\033[0m")
                            date = str(datetime.date(int(remove_split_list[0]), int(
                                remove_split_list[1]), int(remove_split_list[2])))
                        else:
                            date = line

                    except ValueError:
                        date = line
                    except:
                        date = line
                        # print("error")
                    returnlist.append(date)
                    break
        # list(dict.fromkeys(returnlist))
        return returnlist


def regular_expression(branch_name, content, only_one):
    data = load_json_folder('./re_filter_tool/projects/branch_key.json')
    branch = {}
    content = "%" + content.replace("\n", "%↑%") + "%"
    content_in_line = content.split("↑")
    to_datetype_name = ["DateStart", "DateEnd", "ApplyStart", "ApplyEnd"]
    key_list = data[branch_name].keys()
    branch["BranchName"] = branch_name
    if only_one:
        branch_name = "OnlyOne"
    for output_key in key_list:
        branch[output_key] = None
        for key in data[branch_name][output_key]:
            for contentinline in content_in_line:
                findall_list = re.findall(key, contentinline)

                if len(findall_list) != 0:
                    tem = ""
                    while findall_list[0][0] == "%":
                        for i in range(1, len(findall_list[0])):
                            tem += findall_list[0][i]
                        findall_list[0] = tem
                        tem = ""
                    while findall_list[0][len(findall_list[0])-1] == "%":
                        for i in range(0, len(findall_list[0])-1):
                            tem += findall_list[0][i]
                        findall_list[0] = tem
                        tem = ""
                    del_open_character(findall_list)
                if len(findall_list) == 0:
                    findall_list = None
                if branch[output_key] == None:
                    branch[output_key] = findall_list
                elif findall_list != None:
                    for compare_twice in findall_list:
                        if not (compare_twice in branch[output_key]):
                            branch[output_key].append(compare_twice)
        if output_key in to_datetype_name:
            branch[output_key] = to_date_type(
                output_key, branch[output_key], content)
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
        branch_name_list.append("General")
    elif len(branch_name_list) == 1:
        only_one = True

    branches = []
    for branch_name in branch_name_list:
        regular_expression(
            branch_name, content, only_one)
        branches.append(regular_expression(branch_name, content, only_one))

    return branches


def fil_ex_branch(content, ori_sources):
    data = load_json_folder('./re_filter_tool/projects/ex_branch_key.json')
    ex_branch_dic = {}
    content = "%" + content.replace("\n", "%↑%") + "%"
    content_list = content.split("↑")
    ex_branch_name_data = ["Connection", "Holder",
                           "Objective", "Sources", "Subtitle"]
    for key in ex_branch_name_data:
        ex_branch_dic[key] = []
        for value in data[key]:
            for content_in_line in content_list:
                findall_list = re.findall(value, content_in_line)
                if len(findall_list) != 0:
                    tem = ""
                    while findall_list[0][0] == "%":
                        for i in range(1, len(findall_list[0])):
                            tem += findall_list[0][i]
                        findall_list[0] = tem
                        tem = ""
                    while findall_list[0][len(findall_list[0])-1] == "%":
                        for i in range(0, len(findall_list[0])-1):
                            tem += findall_list[0][i]
                        findall_list[0] = tem
                        tem = ""
                    del_open_character(findall_list)
                if len(findall_list) != 0:
                    ex_branch_dic[key].extend(findall_list)
        if len(ex_branch_dic[key]) == 0:
            ex_branch_dic[key] = None
    if ex_branch_dic["Sources"] != None:
        ex_branch_dic["Sources"] = ex_branch_dic["Sources"] + ori_sources
    else:
        ex_branch_dic["Sources"] = ori_sources
    if len(ex_branch_dic["Sources"]) == 0:
        ex_branch_dic["Sources"] = None
    ex_branch_dic["Tags"] = tags_filter(content)

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
    # output_dic["Content"] = obj_dic["content"]
    output_dic["Content"] = obj_dic["content"].replace(" ", "")
    if "image" in obj_dic.keys():
        output_dic["Image"] = obj_dic["image"]
    else:
        output_dic["Image"] = None
    # output_dic["Date"] = obj_dic["date"]
    output_dic.update(fil_ex_branch(output_dic["Content"], tem_sources))
    output_dic["Branches"] = fil_branch(output_dic["Content"])
    return output_dic


# write output json
with open('./re_filter_tool/filter_after.json', 'w', encoding='utf-8') as jsonfile:
    folder_list = ["hunter"]
    # folder_list = ["re_filter_tool"]
    load_folder_list = []
    for folder_name in folder_list:
        folder_name = './projects/index.json'
        load_folder_list += load_json_folder(folder_name)

    output_list = []
    ActivityId = 0
    for each_obj in load_folder_list:
        output_list.append(obj_filter(each_obj))
        output_list[ActivityId]["Id"] = 0  # 0 when put to API
        ActivityId += 1
    # print(output_list)
    json.dump(output_list, jsonfile, ensure_ascii=False, indent=4)
jsonfile.close()

update_only_one()


# filter date from original floder["date"]


# filter "Tags" in except_branch_dic
