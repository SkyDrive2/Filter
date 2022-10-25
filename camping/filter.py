from asyncio.windows_events import NULL
import json
from json import load

# read key txt to list


def read_key_txt(key_location):
    f = open("./camping/filter_keywords/"+key_location, 'r' , encoding = 'utf-8')
    data = f.read().strip()
    data_in_list = data.split("\n")
    # print(data_in_list)
    f.close()
    return data_in_list

# compare content with filter
def compare(key_list, content_list):
    for content in content_list:
        for key in key_list:
            if key in content:
                return content
    return None


# 處理內文
def fil_content(content, dic):
    dic["content"] = content
    content_in_line = content.split("\n")
    # print(content_in_line)
    dic["activity_beg_time"] = compare(read_key_txt("activity_beg_time.txt"), content_in_line)
    dic["activity_end_time"] = compare(read_key_txt("activity_end_time.txt"), content_in_line)
    dic["apply_beg_time"] = compare(read_key_txt("apply_beg_time.txt"), content_in_line)
    dic["apply_end_time"] = compare(read_key_txt("apply_end_time.txt"), content_in_line)
    dic["contact_info"] = compare(read_key_txt("contact_info.txt"), content_in_line)
    dic["cost"] = compare(read_key_txt("cost.txt"), content_in_line)
    dic["host"] = compare(read_key_txt("host.txt"), content_in_line)
    dic["picture"] = compare(read_key_txt("picture.txt"), content_in_line)
    dic["position"] = compare(read_key_txt("position.txt"), content_in_line)
    dic["recruitment_obj"] = compare(read_key_txt("recruitment_obj.txt"), content_in_line)
    dic["sources"] = compare(read_key_txt("sources.txt"), content_in_line)
    dic["subtitle"] = compare(read_key_txt("subtitle.txt"), content_in_line)
    dic["tag"] = compare(read_key_txt("tag.txt"), content_in_line)
    return

# 處理index.json


def fil_obj(obj):
    out_dic = {}
    out_dic["url"] = obj["url"]
    out_dic["title"] = obj["title"]
    out_dic["date"] = obj["date"]
    fil_content(obj["content"], out_dic)
    return out_dic


f = open('./camping/active/index.json', "r", encoding="utf-8")
data = json.load(f)
f.close()

with open('./camping/active/filter_after.json', 'w', encoding='utf-8') as jsonfile:
    out_list = []
    for obj in data:
        out_list.append(fil_obj(obj))
    json.dump(out_list, jsonfile, ensure_ascii=False, indent=4)
jsonfile.close()
