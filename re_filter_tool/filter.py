import json
import re
import copy

# load folder which is under projects


def load_json_folder(folder_road):
    f = open(folder_road, 'r', encoding='utf-8')
    data = json.load(f)
    f.close()
    return data


def update_only_one():
    a = open("./re_filter_tool/projects/index.json", 'r', encoding='utf-8')
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
    b = open("./re_filter_tool/projects/index.json", "w", encoding="utf-8")
    json.dump(out, b, ensure_ascii=False, indent=4)
    b.close()


def compare(key_list, content_list, type):
    value_list = []
    for content in content_list:
        for key in key_list:
            if key in content:
                if type != "Tags":
                    value_list.append(str(content))
                else:
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


def regular_expression(branch_name, content, only_one):
    data = load_json_folder('./re_filter_tool/projects/branch_key.json')
    branch = {}
    key_list = data[branch_name].keys()
    branch["BranchName"] = branch_name
    if only_one:
        for output_key in key_list:
            branch[output_key] = None
            for key in data["OnlyOne"][output_key]:
                findall_list = re.findall(key, content)
                if len(findall_list) == 0:
                    findall_list = None
                if branch[output_key] == None:
                    branch[output_key] = findall_list
                elif findall_list != None:
                    for compare_twice in findall_list:
                        if not (compare_twice in branch[output_key]):
                            branch[output_key].append(compare_twice)
        return branch
    else:
        for output_key in key_list:
            branch[output_key] = None
            for key in data[branch_name][output_key]:
                findall_list = re.findall(key, content)
                if len(findall_list) == 0:
                    findall_list = None
                if branch[output_key] == None:
                    branch[output_key] = findall_list
                elif findall_list != None:
                    for compare_twice in findall_list:
                        if not (compare_twice in branch[output_key]):
                            branch[output_key].append(compare_twice)
        return branch


def fil_except_branch(content, ori_sources):
    data = load_json_folder('./re_filter_tool/projects/ex_branch_key.json')
    content_in_line = content.split("\n")
    except_branch_dic = {}
    except_branch_dic["Connection"] = compare(
        data["connection"], content_in_line, "Connection")
    except_branch_dic["Holder"] = compare(
        data["holder"], content_in_line, "Holder")
    except_branch_dic["Objective"] = compare(
        data["object"], content_in_line, "Object")
    except_branch_dic["Subtitle"] = compare(
        data["subtitle"], content_in_line, "Subtitle")
    update_sources = compare(data["sources"], content_in_line, "Sources")
    if ori_sources == None:
        except_branch_dic["Sources"] = update_sources
    else:
        if update_sources != None:
            except_branch_dic["Sources"] = update_sources.append(
                "ori_sources : " + ori_sources)
    except_branch_dic["Tags"] = tags_filter(content)
    return except_branch_dic


def fil_branch(content):
    content.replace("\n", "%")
    data = load_json_folder('./re_filter_tool/projects/ex_branch_key.json')

    branch_name_list = []
    for branch_name in data["branch_name"]:
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


def obj_filter(obj_dic):
    output_dic = {}
    output_dic["Title"] = obj_dic["title"]
    output_dic["Sources"] = obj_dic["url"]
    output_dic["Content"] = obj_dic["content"].replace(" ", "")
    if "img" in obj_dic.keys():
        output_dic["Image"] = obj_dic["img"]
    # output_dic["Date"] = obj_dic["date"]
    output_dic.update(fil_except_branch(
        output_dic["Content"], output_dic["Sources"]))
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

update_only_one
# testre = re.split("[^0-9]", "哈摟哀呢區111年10月5日")
# ttest = [for i in testre : if i != ]
# print(ttest)


# filter date from original floder["date"]



# filter "Tags" in except_branch_dic