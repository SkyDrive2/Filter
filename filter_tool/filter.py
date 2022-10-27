import json
from json import load

# compare content with filter
def compare(key_list, content_list):
    for content in content_list:
        for key in key_list:
            if key in content:
                return content
    return None

# all key in output
# 課程網址
# 初賽 複賽 線上賽 線下賽
# 活動訊息
def fil_content(content, dic):
    f = open('./filter_tool/filter_key_words.json', "r", encoding="utf-8")
    data = json.load(f)
    f.close()
    dic["content"] = content.replace(" ", "")
    content_in_line = content.split("\n")
    dic["activity_beg_time"] = compare(
        data["activity_beg_time"], content_in_line)
    dic["activity_end_time"] = compare(
        data["activity_end_time"], content_in_line)
    dic["apply_beg_time"] = compare(data["apply_beg_time"], content_in_line)
    dic["apply_end_time"] = compare(data["apply_end_time"], content_in_line)
    dic["apply_int_site"] = compare(data["apply_int_site"], content_in_line)
    dic["contact_info"] = compare(data["contact_info"], content_in_line)
    dic["cost"] = compare(data["cost"], content_in_line)
    dic["host"] = compare(data["host"], content_in_line)
    dic["picture"] = compare(data["picture"], content_in_line)
    dic["position"] = compare(data["position"], content_in_line)
    dic["recruitment_obj"] = compare(data["recruitment_obj"], content_in_line)
    if dic["sources"] == None:
        dic["sources"] = compare(data["sources"], content_in_line)
    dic["subtitle"] = compare(data["subtitle"], content_in_line)
    dic["tag"] = compare(data["tag"], content_in_line)
    return

# handle index.json
def fil_obj(obj):
    out_dic = {}
    out_dic["sources"] = obj["url"]
    out_dic["title"] = obj["title"]
    out_dic["date"] = obj["date"]
    fil_content(obj["content"], out_dic)
    return out_dic

# handle activity folder
def load_json_folder(folder_road):
    f = open('./'+ folder_road + '/projects/index.json', 'r',encoding = 'utf-8')
    data = json.load(f)
    f.close()
    return data

# write output json
with open('./filter_tool/filter_after.json', 'w', encoding='utf-8') as jsonfile:
    load_folder_list = load_json_folder("camping") + load_json_folder("developerWeb") + load_json_folder("peaceHighSchool")
    out_list = []
    for obj in load_folder_list:
        out_list.append(fil_obj(obj))
    json.dump(out_list, jsonfile, ensure_ascii=False, indent=4)
jsonfile.close()
